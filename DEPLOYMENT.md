# Deployment Guide - Antigravity E-Commerce Platform

This guide covers deploying the Antigravity e-commerce platform to production environments.

## 📋 Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] Database backups created
- [ ] Frontend build optimized
- [ ] Backend tested with production database
- [ ] HTTPS certificates ready
- [ ] API rate limiting configured
- [ ] Error logging setup
- [ ] CDN configured (optional)

---

## 🚀 Backend Deployment (Flask on Heroku/Railway)

### Using Heroku

1. **Install Heroku CLI:**
   ```bash
   npm install -g heroku
   heroku login
   ```

2. **Create Heroku app:**
   ```bash
   cd backend
   heroku create antigravity-api
   ```

3. **Configure environment variables:**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY="your-secure-secret-key"
   heroku config:set JWT_EXPIRATION_HOURS=24
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Check logs:**
   ```bash
   heroku logs --tail
   ```

### Using Railway.app

1. **Connect repository to Railway**
2. **Set environment variables in Railway dashboard**
3. **Deploy from dashboard or push to GitHub**

### Using AWS/DigitalOcean

1. **Create server instance**
2. **Install Python, pip, and dependencies**
3. **Configure Gunicorn:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
4. **Setup Nginx reverse proxy**
5. **Configure SSL with Let's Encrypt**

---

## 🎨 Frontend Deployment (React/Vite)

### Using Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd frontend
   vercel
   ```

3. **Configure environment:**
   - Set `VITE_API_URL` to your backend API URL
   - Automatic CI/CD on git push

### Using Netlify

1. **Connect GitHub repository to Netlify**
2. **Configure build settings:**
   - Build command: `npm run build`
   - Publish directory: `dist`
3. **Set environment variables**
4. **Deploy automatically on push**

### Using AWS S3 + CloudFront

1. **Build the application:**
   ```bash
   npm run build
   ```

2. **Upload to S3:**
   ```bash
   aws s3 sync dist/ s3://your-bucket-name
   ```

3. **Configure CloudFront distribution**
4. **Set cache headers for optimal performance**

### Using Docker

1. **Create Dockerfile:**
   ```dockerfile
   FROM node:18-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build
   
   FROM nginx:alpine
   COPY --from=0 /app/dist /usr/share/nginx/html
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

2. **Build and push to Docker Hub:**
   ```bash
   docker build -t antigravity-frontend .
   docker push your-registry/antigravity-frontend
   ```

---

## 🔐 Security Configuration

### Backend Security

1. **Update Flask config:**
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True
   app.config['SESSION_COOKIE_HTTPONLY'] = True
   app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
   ```

2. **Enable HTTPS**
3. **Configure CORS properly:**
   ```python
   CORS(app, origins=['https://your-domain.com'])
   ```

4. **Set security headers**
5. **Implement rate limiting**

### Frontend Security

1. **Content Security Policy headers**
2. **Remove debug information from production build**
3. **Enable HTTPS only**
4. **Implement XSRF protection**

---

## 🗄️ Database Configuration

### Using JSON Files (Current)
- Files stored in root directory
- Backup regularly using cron jobs
- Suitable for small deployments

### Migration to PostgreSQL (Recommended)

1. **Install PostgreSQL adapter:**
   ```bash
   pip install psycopg2-binary sqlalchemy
   ```

2. **Update Flask app:**
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
   ```

3. **Migrate data from JSON to database**

---

## 📊 Monitoring & Logging

### Application Monitoring

- **Sentry** for error tracking
- **New Relic** for performance monitoring
- **DataDog** for infrastructure metrics

### Setup Sentry (Backend):

```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

### Logging

```python
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

---

## 📈 Performance Optimization

### Backend

1. **Enable gzip compression:**
   ```python
   from flask_compress import Compress
   Compress(app)
   ```

2. **Implement caching:**
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'redis'})
   ```

3. **Optimize database queries**
4. **Use connection pooling**

### Frontend

1. **Code splitting:**
   ```javascript
   // Vite auto-handles this
   ```

2. **Image optimization**
3. **Enable compression**
4. **Use CDN for assets**

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy Backend
      run: |
        git push heroku main
    
    - name: Deploy Frontend
      run: |
        cd frontend
        npm install
        npm run build
        vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

---

## 🆘 Troubleshooting Deployment

### Issue: CORS errors
**Solution:** Configure CORS origins in Flask

### Issue: 504 Gateway Timeout
**Solution:** Increase timeout settings, optimize queries

### Issue: Out of memory
**Solution:** Use worker processes, implement caching

### Issue: Database connection errors
**Solution:** Check connection string, verify credentials

---

## 📋 Production Checklist

- [ ] Change default secret keys
- [ ] Enable HTTPS
- [ ] Configure backups
- [ ] Setup monitoring
- [ ] Test all features
- [ ] Configure email notifications
- [ ] Setup error alerts
- [ ] Document deployment process
- [ ] Create rollback procedure
- [ ] Test database restore
- [ ] Performance test under load
- [ ] Security audit completed

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks

- Weekly: Backup database
- Monthly: Review logs and errors
- Quarterly: Security updates
- Annually: Full system audit

### Emergency Procedures

1. **Database recovery**: Use backup files
2. **API down**: Switch to backup server
3. **Severe bugs**: Rollback to previous version

---

## 📚 Reference Links

- [Heroku Deployment](https://devcenter.heroku.com/articles/deploying-python)
- [Vercel Documentation](https://vercel.com/docs)
- [Railway.app Guide](https://docs.railway.app)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices)
- [Flask Production Guide](https://flask.palletsprojects.com/en/2.3.x/tutorial/deploy/)

---

**Last Updated:** 2024
**Version:** 1.0.0
