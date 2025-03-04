'use client';

import React, { useState, useRef, useEffect } from 'react';
import { pdfjs, Document, Page } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';
import {Row, Col, Typography, Button} from "antd";

const { Paragraph } = Typography;

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

interface PDFViewerProps {
  pdfUrl: string;
}

const PDFViewer: React.FC<PDFViewerProps> = ({ pdfUrl }) => {
  const [numPages, setNumPages] = useState<number | null>(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [pageWidth, setPageWidth] = useState(0);
  const containerRef = useRef<HTMLDivElement | null>(null);

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
  };

  const goToPrevPage = () => setPageNumber(pageNumber - 1);
  const goToNextPage = () => setPageNumber(pageNumber + 1);

    useEffect(() => {
    const updatePageWidth = () => {
      if (containerRef.current) {
        setPageWidth(containerRef.current.clientWidth);
      }
    };

    updatePageWidth();
    window.addEventListener('resize', updatePageWidth);
    return () => window.removeEventListener('resize', updatePageWidth);
  }, []);

  return (
    <div ref={ containerRef } style={{ flexGrow: 1, margin: '10px 0'}}>
      <Row style={{ flexGrow: 1 }} gutter={12}>
        <Document
          file={pdfUrl}
          onLoadSuccess={onDocumentLoadSuccess}
        >
          <Page pageNumber={pageNumber} width={pageWidth} />
        </Document>
      </Row>

      {pageNumber && <Row gutter={12} style={{paddingTop: '6px'}}>
          <Col>
              <Paragraph>Page {pageNumber} / {numPages}</Paragraph>
          </Col>
          <Col style={{paddingTop: '1px'}}>
            <Button onClick={goToPrevPage} disabled={pageNumber <= 1} style={{padding: '4px', height: '20px'}}>
              Previous
            </Button>
          </Col>
          <Col style={{paddingTop: '1px'}}>
            <Button onClick={goToNextPage} disabled={numPages ? pageNumber >= numPages : false} style={{padding: '4px', height: '20px'}}>
              Next
            </Button>
          </Col>
      </Row>}
    </div>
  );
};

export default PDFViewer;
