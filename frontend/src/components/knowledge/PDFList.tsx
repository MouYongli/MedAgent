import React from 'react';
import { List, Checkbox } from 'antd';

interface PDFItem {
  id: string;
  name: string;
  url: string;
}

interface PDFListProps {
  pdfList: PDFItem[];
  selectedPdfId: string | null;
  onSelectPdf: (id: string | null) => void;
}

const PDFList: React.FC<PDFListProps> = ({
  pdfList,
  selectedPdfId,
  onSelectPdf,
}) => {
  const handleCheckboxChange = (id: string) => {
    if (selectedPdfId === id) {
      onSelectPdf(null); // Unselect if already selected
    } else {
      onSelectPdf(id); // Select new item
    }
  };

  return (
    <List
      dataSource={pdfList}
      renderItem={item => (
        <List.Item style={{ borderBottom: 'none', padding: '8px 0' }}>
          <Checkbox
            checked={selectedPdfId === item.id}
            onChange={() => handleCheckboxChange(item.id)}
          >
            {item.name}
          </Checkbox>
        </List.Item>
      )}
      style = {{ margin: '10px 0' }}
    />
  );
};

export default PDFList;
