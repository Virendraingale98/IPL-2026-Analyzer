# Flask-CORS import missing error fix

In backend/app.py, add this import at the top:

```python
from flask_cors import CORS
```

Install CORS support if not already installed:
```bash
pip install flask-cors
```

Then update requirements.txt to include:
```
Flask-CORS==4.0.0
```
