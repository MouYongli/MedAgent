import React, { useState } from 'react';
import { Button, Modal, Upload, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';


interface UploadPDButtonProps {
  onUploadPdf: (file: File) => void;
}

const UploadPDFButton: React.FC<UploadPDButtonProps> = ({
  onUploadPdf,
}) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [fileList, setFileList] = useState<any[]>([]);

  const handleUploadChange = ({ file, fileList }: any) => {
    if (file.status === 'done') {
      message.success(`${file.name} file uploaded successfully.`);
      onUploadPdf(file.originFileObj);
      setIsModalVisible(false);
      setFileList([]);
    } else if (file.status === 'error') {
      message.error(`${file.name} file upload failed.`);
    } else {
      setFileList(fileList);
    }
  };

  return (
    <div>
      <Button type="primary" onClick={() => setIsModalVisible(true)}>
        Upload New PDF
      </Button>
      <Modal
        title="Upload PDF"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
      >
        <Upload
          accept=".pdf"
          beforeUpload={() => false} // Prevent automatic upload
          fileList={fileList}
          onChange={handleUploadChange}
        >
          <Button icon={<UploadOutlined />}>Select PDF</Button>
        </Upload>
      </Modal>
    </div>
  );
};

export default UploadPDFButton;
