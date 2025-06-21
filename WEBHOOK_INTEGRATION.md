# Webhook Integration with Meetstream

This document explains how to connect your Meetstream transcription service with the Steel Merchant Inventory System using webhooks.

## Overview

The system now supports real-time transcription updates from Meetstream through webhook integration. When Meetstream sends a transcription, it will automatically appear on the website and can be used to generate cart items.

## Architecture

```
Meetstream → Webhook Server (Port 5001) → Main App (Port 5000) → Website Display
```

1. **Meetstream** sends transcriptions to the webhook server
2. **Webhook Server** receives and forwards transcriptions to the main app
3. **Main App** stores transcriptions and displays them on the website
4. **Website** shows real-time transcription updates

## Setup Instructions

### 1. Start Both Servers

Run the following command to start both servers simultaneously:

```bash
python run_servers.py
```

This will start:
- **Main App**: http://localhost:5000
- **Webhook Server**: http://localhost:5001

### 2. Configure Meetstream Webhook

In your Meetstream settings, configure the webhook URL to:

```
http://localhost:5001/transcription
```

**Supported Payload Formats:**
- `{"transcript": "your transcription text"}`
- `{"data": {"text": "your transcription text"}}`
- `{"data": {"transcription": "your transcription text"}}`
- `{"text": "your transcription text"}`

### 3. Test the Integration

Use the provided test script to simulate webhook requests:

```bash
python test_webhook.py
```

This will allow you to:
- Send random sample transcriptions
- Send custom transcriptions
- Send multiple transcriptions for testing

## Features

### Real-time Updates
- Transcriptions appear on the website within 2 seconds
- Visual highlight animation when new transcriptions arrive
- Transcription history (last 10 transcriptions)

### User Interface
- **Left Panel**: Shows latest transcription and history
- **Right Panel**: Manual entry form for transcriptions
- **"Use Latest Transcription"** button to populate the form

### Webhook Endpoints

#### Receive Transcription
- **URL**: `POST /receive_transcription`
- **Content-Type**: `application/json`
- **Payload**: `{"transcript": "transcription text"}`

#### Get Latest Transcription
- **URL**: `GET /get_latest_transcription`
- **Response**: JSON with latest transcription and history

## Troubleshooting

### Common Issues

1. **Webhook server not receiving requests**
   - Check if webhook server is running on port 5001
   - Verify Meetstream webhook URL configuration
   - Check firewall settings

2. **Transcriptions not appearing on website**
   - Ensure main app is running on port 5000
   - Check browser console for JavaScript errors
   - Verify network connectivity between servers

3. **Connection errors**
   - Make sure both servers are running
   - Check if ports 5000 and 5001 are available
   - Restart servers if needed

### Logs

Both servers provide detailed logging:

- **Webhook Server**: Shows incoming requests and forwarding status
- **Main App**: Shows received transcriptions and processing

### Testing

Use the test script to verify the integration:

```bash
python test_webhook.py
```

This will help you:
- Verify webhook server is working
- Test different payload formats
- Simulate real transcription scenarios

## Security Considerations

- The webhook server accepts any JSON payload
- Consider adding authentication for production use
- Validate transcription content before processing
- Implement rate limiting for webhook endpoints

## Production Deployment

For production deployment:

1. **Use HTTPS**: Configure SSL certificates for secure webhook communication
2. **Authentication**: Add API keys or webhook signatures
3. **Rate Limiting**: Implement request throttling
4. **Logging**: Set up proper logging and monitoring
5. **Error Handling**: Add comprehensive error handling and retry logic

## Support

If you encounter issues:

1. Check the server logs for error messages
2. Verify Meetstream webhook configuration
3. Test with the provided test script
4. Ensure both servers are running and accessible 