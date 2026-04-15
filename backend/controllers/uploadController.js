const path = require('path');
const fs = require('fs');

/**
 * Handles the document upload process.
 * Stores the file in the 'uploads' directory.
 */
const uploadDocument = (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({
                success: false,
                message: "No file uploaded. Please upload a PDF document."
            });
        }

        res.status(200).json({
            success: true,
            message: "File uploaded successfully",
            filename: req.file.filename,
            originalName: req.file.originalname,
            path: `/uploads/${req.file.filename}`
        });
    } catch (error) {
        console.error("Upload Controller Error:", error);
        res.status(500).json({
            success: false,
            message: "Error during file upload",
            error: error.message
        });
    }
};

module.exports = {
    uploadDocument
};
