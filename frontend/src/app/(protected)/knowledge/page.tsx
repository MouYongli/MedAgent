'use client';

import React, { useEffect, useState } from 'react';
import { Box, Container, Typography, List, ListItemButton, ListItemText, Divider, Paper, CircularProgress } from '@mui/material';
import axios from 'axios';
import { Worker, Viewer } from '@react-pdf-viewer/core';
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';
import { zoomPlugin } from '@react-pdf-viewer/zoom';
import { highlightPlugin, Highlight, RenderHighlightContentProps, RenderHighlightsProps } from '@react-pdf-viewer/highlight';

// 导入样式
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';
import '@react-pdf-viewer/zoom/lib/styles/index.css';
import '@react-pdf-viewer/highlight/lib/styles/index.css';

// 导入 worker
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.entry';

interface PdfFile {
  name: string;
  selected: boolean;
}

// 高亮数据接口
interface HighlightArea {
  pageIndex: number;
  bounds: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
}

// 扩展 Highlight 接口以满足需求
interface CustomHighlight extends Highlight {
  id: string;
  comment?: string;
  createdAt: Date;
}

const KnowledgePage: React.FC = () => {
  const [pdfFiles, setPdfFiles] = useState<PdfFile[]>([]);
  const [selectedPdf, setSelectedPdf] = useState<string | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [highlights, setHighlights] = useState<CustomHighlight[]>([]);

  // 创建插件实例
  const defaultLayoutPluginInstance = defaultLayoutPlugin();
  const zoomPluginInstance = zoomPlugin();
  const highlightPluginInstance = highlightPlugin({
    onHighlightClick: (highlight: Highlight) => {
      console.log('Highlight clicked:', highlight);
    },
    renderHighlightContent: (props: RenderHighlightContentProps) => (
      <div style={{ background: 'yellow', opacity: 0.4 }} />
    ),
    onHighlightAdd: (highlight: Highlight) => {
      const newHighlight: CustomHighlight = {
        ...highlight,
        id: `highlight-${Date.now()}`,
        createdAt: new Date(),
      };
      setHighlights((prev) => [...prev, newHighlight]);
      return newHighlight;
    },
    renderHighlights: (props: RenderHighlightsProps) => {
      const { highlightsByPage, scale } = props;
      const pageIndex = props.pageIndex;
      
      // 确保 highlightsByPage 和对应的页面索引存在
      if (!highlightsByPage || !highlightsByPage[pageIndex]) {
        return <></>;
      }
      
      const pageHighlights = highlightsByPage[pageIndex];
      
      return (
        <>
          {pageHighlights.map((highlight) => {
            // 检查 highlight 和必要的属性是否存在
            if (!highlight || !highlight.position || !highlight.position.boundingRect) {
              return null;
            }
            
            return (
              <div
                key={highlight.id || Math.random().toString()}
                style={{
                  position: 'absolute',
                  left: highlight.position.boundingRect.x * scale,
                  top: highlight.position.boundingRect.y * scale,
                  width: highlight.position.boundingRect.width * scale,
                  height: highlight.position.boundingRect.height * scale,
                  background: 'yellow',
                  opacity: 0.4,
                }}
                onClick={() => highlightPluginInstance.jumpToHighlight(highlight)}
              />
            );
          })}
        </>
      );
    },
  });

  useEffect(() => {
    const fetchPdfFiles = async () => {
      try {
        const response = await axios.get(`${process.env.NEXT_PUBLIC_BACKEND_URL}:${process.env.NEXT_PUBLIC_BACKEND_PORT}/api/knowledge/pdf`);
        const files = response.data.map((file: string) => ({
          name: file,
          selected: false
        }));
        setPdfFiles(files);
      } catch (error) {
        console.error('Error fetching PDF files:', error);
      }
    };

    fetchPdfFiles();
  }, []);

  const handlePdfSelect = async (pdfName: string) => {
    setSelectedPdf(pdfName);
    setPdfFiles(pdfFiles.map(file => ({
      ...file,
      selected: file.name === pdfName
    })));

    try {
      setIsLoading(true);
      // 构建 PDF 文件的 URL
      const pdfFileUrl = `${process.env.NEXT_PUBLIC_BACKEND_URL}:${process.env.NEXT_PUBLIC_BACKEND_PORT}/api/knowledge/pdf/${pdfName}`;
      setPdfUrl(pdfFileUrl);
    } catch (error) {
      console.error('Error loading PDF:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxWidth={false} sx={{ py: 3 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Knowledge Base
      </Typography>
      <Divider sx={{ mb: 3 }} />

      <Box sx={{ display: 'flex', height: 'calc(100vh - 200px)', gap: 2 }}>
        {/* 左侧 PDF 列表 */}
        <Paper sx={{ width: '30%', overflow: 'auto', p: 2 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            PDF Files
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <List>
            {pdfFiles.map((file) => (
              <ListItemButton
                key={file.name}
                selected={file.selected}
                onClick={() => handlePdfSelect(file.name)}
                sx={{
                  borderRadius: 1,
                  mb: 1,
                  '&.Mui-selected': {
                    backgroundColor: 'primary.light',
                    '&:hover': {
                      backgroundColor: 'primary.light',
                    }
                  }
                }}
              >
                <ListItemText 
                  primary={file.name}
                  primaryTypographyProps={{
                    sx: { 
                      color: file.selected ? 'primary.contrastText' : 'inherit'
                    }
                  }}
                />
              </ListItemButton>
            ))}
          </List>
        </Paper>

        {/* 右侧 PDF 查看区域 */}
        <Paper sx={{ width: '70%', p: 2 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            PDF Viewer
          </Typography>
          <Divider sx={{ mb: 2 }} />
          {!selectedPdf ? (
            <Box sx={{ 
              height: '100%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center' 
            }}>
              <Typography variant="body1" color="text.secondary">
                请选择左侧的 PDF 文件进行查看
              </Typography>
            </Box>
          ) : isLoading ? (
            <Box sx={{ 
              height: '100%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center' 
            }}>
              <CircularProgress />
            </Box>
          ) : (
            <Box sx={{ height: 'calc(100% - 60px)' }}>
              <Worker workerUrl={pdfjsWorker}>
                {pdfUrl && (
                  <Viewer
                    fileUrl={pdfUrl}
                    plugins={[
                      defaultLayoutPluginInstance,
                      zoomPluginInstance,
                      highlightPluginInstance,
                    ]}
                  />
                )}
              </Worker>
            </Box>
          )}
        </Paper>
      </Box>
    </Container>
  );
};

export default KnowledgePage;
