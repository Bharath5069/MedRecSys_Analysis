import React, { useState } from 'react';
import { Upload, message, Button } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const PDFUploader = () => {
    const [loading, setLoading] = useState(false);

    const handleUpload = async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            setLoading(true);
            const response = await fetch('http://localhost:8000/api/v1/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            const data = await response.json();
            message.success('File uploaded successfully');
            return data;
        } catch (error) {
            message.error('Upload failed: ' + error.message);
            return null;
        } finally {
            setLoading(false);
        }
    };

    const uploadProps = {
        name: 'file',
        accept: '.pdf',
        beforeUpload: (file) => {
            handleUpload(file);
            return false; // Prevent default upload behavior
        },
        showUploadList: false,
    };

    return (
        <Upload {...uploadProps}>
            <Button icon={<UploadOutlined />} loading={loading}>
                Upload PDF
            </Button>
        </Upload>
    );
};

export default PDFUploader; 