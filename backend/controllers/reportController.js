const axios = require('axios');

/**
 * Triggers the Python AI service to generate a Credit Appraisal Memo (CAM).
 */
const generateReport = async (req, res) => {
    const { analysisData } = req.body;

    // Optional: analysisData could be used to customize the report, 
    // but the requirement says the Python service handles it.
    
    try {
        const pythonServiceUrl = 'http://localhost:8000/generate-cam';
        const response = await axios.post(pythonServiceUrl, analysisData || {});

        res.status(200).json({
            success: true,
            message: "CAM report generated",
            file: response.data.file || "CAM_Report.pdf",
            path: response.data.path
        });
    } catch (error) {
        console.error("Report Controller Error:", error.message);

        let errorMessage = "Python AI Service failure during report generation";
        if (error.code === 'ECONNREFUSED') {
            errorMessage = "Python AI Service is not running. Please start it on port 8000.";
        }

        res.status(500).json({
            success: false,
            message: errorMessage,
            error: error.message
        });
    }
};

module.exports = {
    generateReport
};
