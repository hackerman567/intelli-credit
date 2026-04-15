const express = require('express');
const router = express.Router();
const analysisController = require('../controllers/analysisController');

/**
 * @route   POST /api/analyze
 * @desc    Extract financial data and calculate risk
 * @access  Public
 */
router.post('/', analysisController.analyzeDocument);
router.post('/simulate', analysisController.simulateCredit);

module.exports = router;
