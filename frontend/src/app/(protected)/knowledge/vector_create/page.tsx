'use client';

import React, { useState } from 'react';
import dynamic from "next/dynamic";
import {Row, Col, Typography, Divider, message} from 'antd';
import PDFList from "@/components/knowledge/PDFList";
import UploadPDFButton from "@/components/knowledge/UploadPDFButton";

const PDFViewer = dynamic(() => import('@/components/knowledge/PDFViewer'), { ssr: false });

const { Title, Paragraph } = Typography;

const VectorCreatePage: React.FC = () => {
  const [pdfList, setPdfList] = useState([
    { id: '0', name: 'Document 0', url: '/pdfs/0.pdf' },
    { id: '1', name: 'Document 1', url: '/pdfs/1.pdf' },
  ]);
  const [selectedPdfId, setSelectedPdfId] = useState<string | null>(null);

  const handleSelectPdf = (id: string | null) => {
    setSelectedPdfId(id);
  };

  const handleUploadPdf = (file: File) => {
    const newPdf = { id: file.name, name: file.name, url: URL.createObjectURL(file) };
    setPdfList([...pdfList, newPdf]);
    message.success(`${file.name} uploaded successfully.`);
  };

  const selectedGuideline = pdfList.find(pdf => pdf.id === selectedPdfId)?.name || "Select guideline";
  const selectedPdfUrl = pdfList.find(pdf => pdf.id === selectedPdfId)?.url || null;

  return (
    <div>
      <Title level={2}>Create new vector database</Title>
      <Paragraph>
        Create a new vector database by uploading PDFs, chunking them, and ultimately storing them in a vector database.
      </Paragraph>
      <Divider />
      <Row gutter={[12, 0]}> {/* Sections for vector indexing: Guidelines, Chunk creation, Chunk on PDF display */}
        {/* !! TODO: gutter is currently not working !! Therefore, added the margin solution, but might need redo this */}
        <Col span={5} style={{ backgroundColor: '#f5f5f5', borderRadius: '12px', padding: '16px', margin: '0 6px' }}>
          <Title level={3} style={{ marginBlock: '0' }}>Guidelines</Title>
          <PDFList pdfList={pdfList} selectedPdfId={selectedPdfId} onSelectPdf={handleSelectPdf} />
          <UploadPDFButton onUploadPdf={handleUploadPdf} />
        </Col>
        <Col span={8} style={{ backgroundColor: '#f5f5f5', borderRadius: '12px', padding: '16px', margin: '0 6px' }}>
          <Title level={3} style={{ marginBlock: '0' }}>{ selectedGuideline }</Title>
        </Col>
        <Col style={{ backgroundColor: '#f5f5f5', borderRadius: '12px', padding: '16px', margin: '0 6px', flexGrow: 1 }}>
          <Title level={3} style={{ marginBlock: '0' }}>PDF display</Title>
          {selectedPdfUrl ? (<div>
            <PDFViewer pdfUrl={selectedPdfUrl} />
          </div>) : (
            <Paragraph>Select a guideline to view the PDF</Paragraph>
          )}
        </Col>
      </Row>
    </div>
  );
};

export default VectorCreatePage;
