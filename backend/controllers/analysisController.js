const axios = require('axios');

/**
 * Sends the filename to the Python AI service for financial analysis.
 */
const analyzeDocument = async (req, res) => {
    const { filename, company_name, promoter_name, officer_notes, sector } = req.body;

    if (!filename || !company_name) {
        return res.status(400).json({
            success: false,
            message: "Missing required fields: filename and company_name."
        });
    }

    try {
        const pythonServiceUrl = 'http://localhost:8000/analyze';
        const response = await axios.post(pythonServiceUrl, { 
            filename, 
            company_name, 
            promoter_name: promoter_name || "Rajesh Sharma",
            officer_notes,
            sector
        });

        res.status(200).json({
            success: true,
            message: "Analysis completed successfully",
            data: response.data
        });
    } catch (error) {
        console.error("Analysis Controller Error:", error.message);
        let errorMessage = "Python AI Service failure";
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

const simulateCredit = async (req, res) => {
    try {
        const pythonServiceUrl = 'http://localhost:8000/simulate';
        const response = await axios.post(pythonServiceUrl, req.body);

        res.status(200).json({
            success: true,
            data: response.data
        });
    } catch (error) {
        console.error("Simulation Controller Error:", error.message);
        res.status(500).json({
            success: false,
            message: "Simulation failure",
            error: error.message
        });
    }
};

module.exports = {
    analyzeDocument,
    simulateCredit
};
