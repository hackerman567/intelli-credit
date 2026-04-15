const express = require('express');
const router = express.Router();
const reportController = require('../controllers/reportController');

/**
 * @route   POST /api/report
 * @desc    Generate Credit Appraisal Memo (CAM)
 * @access  Public
 */
router.post('/', reportController.generateReport);

module.exports = router;
