# Book Rental Backend API

A robust Node.js/Express backend for managing book rentals with Shopify integration and Supabase database.

## 🚀 Features

### Core Functionality
- **Rental Management**: Create, update, and track book rentals
- **Shopify Integration**: Product and cart management
- **Webhook Processing**: Automatic rental record creation from Shopify orders
- **Customer Management**: Track customer plans and rental limits
- **Return/Replace System**: Advanced book replacement system

### Technical Features
- **Bulletproof Error Handling**: Comprehensive validation and error recovery
- **Health Monitoring**: Detailed health checks for all services
- **Graceful Shutdown**: Proper cleanup on server termination
- **Comprehensive Logging**: Detailed request/response logging
- **CORS Support**: Configurable cross-origin resource sharing
- **Rate Limiting**: Built-in request throttling

## 📋 Prerequisites

- Node.js 18+ 
- Supabase account and database
- Shopify store with Admin API access
- Environment variables configured

## 🔧 Environment Variables

Create a `.env` file with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key

# Shopify Configuration
SHOPIFY_STORE=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_admin_access_token
SHOPIFY_STOREFRONT_TOKEN=your_storefront_token
SHOPIFY_LOCATION_ID=your_location_id

# Server Configuration
PORT=3000
NODE_ENV=production
ALLOWED_ORIGINS=https://yourdomain.com,https://anotherdomain.com
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd book-rental-backend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Start the server**
   ```bash
   npm start
   ```

## 🧪 Testing

### Run All Tests
```bash
npm test
```

### Run Local Tests
```bash
npm run test:local
```

### Test Coverage
The test suite covers:
- ✅ Health checks
- ✅ API endpoints
- ✅ Error handling
- ✅ Data validation
- ✅ Webhook processing
- ✅ Database operations

## 📚 API Endpoints

### Health & Monitoring
- `GET /` - Basic health check
- `GET /health` - Health status
- `GET /health/detailed` - Comprehensive health check

### Core API
- `GET /api/plan` - Get customer plan and limits
- `GET /api/books` - List all available books
- `GET /api/returns` - List active rentals
- `POST /api/order` - Create new rental order
- `POST /api/returns` - Process book returns

- `POST /api/make-new-rental` - Process rental changes

### Webhooks
- `POST /webhook` - Shopify order webhook
- `POST /webhook-verify` - Webhook verification
- `POST /test-webhook` - Test webhook endpoint

### Testing & Debug
- `GET /api/test-table-structure` - Test database structure
- `POST /api/test-rental` - Test rental creation
- `POST /test-webhook` - Test webhook processing

## 🔄 Make New Rental Flow

The `make-new-rental` endpoint handles complex rental replacement logic:

1. **Validation**: Comprehensive input validation
2. **Checkout Creation**: Creates Shopify cart for new books
3. **Database Cleanup**: Deletes old rental records
4. **Record Creation**: Creates new records for kept books
5. **Response**: Returns checkout URL or success confirmation

### Request Format
```json
{
  "customer_id": "customer_123",
  "newBooks": [
    {
      "variantId": "123",
      "title": "New Book",
      "imageUrl": "https://..."
    }
  ],
  "removedBooks": [
    {
      "variantId": "456",
      "title": "Removed Book",
      "imageUrl": "https://..."
    }
  ],
  "currentRentalBooks": [
    {
      "variantId": "789",
      "title": "Kept Book",
      "imageUrl": "https://..."
    }
  ]
}
```

### Response Format
```json
{
  "success": true,
  "message": "Rental changes processed successfully",
  "checkoutUrl": "https://checkout.shopify.com/...",
  "changes": {
    "newBooks": 1,
    "removedBooks": 1,
    "keptBooks": 1
  }
}
```

## 🛡️ Error Handling

### Input Validation
- Required field validation
- Data type checking
- Array validation
- Business logic validation

### Checkout Resilience
- The `/order` endpoint accepts a list of variant IDs (or an `items` array for backwards compatibility).  it simply hands whatever is received to Shopify's cart API without pre‑filtering.  the goal is to **always create a checkout**; if Shopify fails to build a cart the API returns `success:false` and the frontend keeps the cart intact so the customer can retry.
- `/product-status` still exists for informational purposes, but it no longer blocks adds or disables buttons. transients are ignored, and the server will not drop books before attempting checkout.
- The backend no longer attempts to resolve product IDs or perform multiple retries; complexity has been removed in favor of a straight‑through flow.  Shopify is responsible for validating the line items.
- Responses include `removedIds` if Shopify silently discarded any lines, but this is advisory only.

### Error Recovery
- Graceful degradation
- Partial operation completion
- Detailed error logging
- User-friendly error messages

### Error Response Format
```json
{
  "error": "Error description",
  "message": "Detailed error message",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

## 📊 Monitoring

### Health Checks
- Server status monitoring
- Database connectivity
- Shopify API connectivity
- Service dependencies

### Logging
- Request/response logging
- Error tracking
- Performance monitoring
- Debug information

## 🚀 Deployment

### Render Deployment
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

### Environment Variables for Production
```env
NODE_ENV=production
PORT=10000
ALLOWED_ORIGINS=https://yourdomain.com
```

### Health Check URLs
- Basic: `https://your-app.onrender.com/`
- Detailed: `https://your-app.onrender.com/health/detailed`

## 🔧 Development

### Development Mode
```bash
npm run dev
```

### Code Structure
```
src/
├── api/
│   └── routes.js          # API route definitions
├── utils/
│   ├── handlers.js        # Business logic handlers
│   └── shopify.js         # Shopify API integration
├── server.js              # Express server setup
└── test-backend.js        # Comprehensive test suite
```

### Adding New Endpoints
1. Add handler function in `src/utils/handlers.js`
2. Add route in `src/api/routes.js`
3. Add test in `test-backend.js`
4. Update documentation

## 🐛 Troubleshooting

### Common Issues

**Server won't start**
- Check environment variables
- Verify port availability
- Check for missing dependencies

**Database connection errors**
- Verify Supabase credentials
- Check network connectivity
- Validate database schema

**Shopify API errors**
- Verify API tokens
- Check store permissions
- Validate location ID

**Webhook issues**
- Check webhook URL configuration
- Verify webhook signature
- Test with webhook verification endpoint

### Debug Mode
Enable detailed logging:
```bash
DEBUG=* npm start
```

## 📈 Performance

### Optimization Features
- Connection pooling
- Request caching
- Error rate limiting
- Graceful degradation

### Monitoring
- Response time tracking
- Error rate monitoring
- Resource usage tracking
- Health check alerts

## 🔒 Security

### Security Features
- Input sanitization
- CORS protection
- Rate limiting
- Error message sanitization
- Environment variable protection

### Best Practices
- Use HTTPS in production
- Validate all inputs
- Sanitize error messages
- Monitor for suspicious activity
- Regular security updates

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation
- Run the test suite for debugging
