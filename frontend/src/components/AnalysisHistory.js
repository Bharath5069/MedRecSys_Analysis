import React, { useState, useEffect } from 'react';
import { Card, Typography, List, Spin, Alert } from 'antd';
import { FileTextOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const AnalysisHistory = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [analysis, setAnalysis] = useState(null);

    useEffect(() => {
        fetchAnalysis();
    }, []);

    const fetchAnalysis = async () => {
        try {
            setLoading(true);
            const response = await fetch('http://localhost:8000/api/v1/analysis');
            if (!response.ok) {
                throw new Error('Failed to fetch analysis');
            }
            const data = await response.json();
            console.log('Analysis History Data:', data);
            setAnalysis(data.analysis);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div style={{ textAlign: 'center', padding: '20px' }}>
                <Spin size="large" />
            </div>
        );
    }

    if (error) {
        return (
            <Alert
                message="Error"
                description={error}
                type="error"
                showIcon
            />
        );
    }

    if (!analysis || analysis.status === "No recent analysis available") {
        return (
            <Card>
                <Title level={4}>Analysis History</Title>
                <Text type="secondary">No analysis available. Upload a PDF to get started.</Text>
            </Card>
        );
    }

    // Process treatment plan data
    const treatmentPlanContent = analysis.treatment_plan ? (
        <div>
            <Text strong>Recommendations:</Text>
            <Text style={{ display: 'block', marginBottom: '8px' }}>
                {typeof analysis.treatment_plan.recommendations === 'string' 
                    ? analysis.treatment_plan.recommendations 
                    : 'No specific recommendations provided'}
            </Text>
            {analysis.treatment_plan.confidence_score && (
                <Text type="secondary" style={{ display: 'block' }}>
                    Confidence Score: {(analysis.treatment_plan.confidence_score * 100).toFixed(1)}%
                </Text>
            )}
        </div>
    ) : 'No treatment plan available';

    return (
        <Card>
            <Title level={4}>Latest Analysis</Title>
            <List
                itemLayout="horizontal"
                dataSource={[
                    {
                        title: 'Original File',
                        content: analysis.original_filename
                    },
                    {
                        title: 'Timestamp',
                        content: new Date(analysis.timestamp).toLocaleString()
                    },
                    {
                        title: 'Treatment Plan',
                        content: treatmentPlanContent
                    }
                ]}
                renderItem={item => (
                    <List.Item>
                        <List.Item.Meta
                            avatar={<FileTextOutlined />}
                            title={item.title}
                            description={item.content}
                        />
                    </List.Item>
                )}
            />
        </Card>
    );
};

export default AnalysisHistory; 