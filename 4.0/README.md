# Academic Assessment System

A web-based academic assessment management system that enables teachers to register, login, enter student marks, and analyze performance with intelligent categorization and visual dashboards.

## Features

- **User Authentication**: Registration and login system for multiple teachers
- **Exam Data Entry**: Enter department, academic year, internal assessment type, subject, and exam date
- **Student Marks Management**: Dynamic form generation for multiple students with absent handling
- **Performance Analysis**: 
  - Total students, present count, absent count
  - Highest, lowest, and average marks calculation
  - Ranked student list from highest to lowest
- **Color-Coded Performance Indicators**:
  - 🟢 Green: High performers (>10 above average)
  - 🟡 Yellow: Average performers
  - 🔴 Red: Students requiring attention (<10 below average)
- **Data Persistence**: All user accounts and exam records stored in JSON files

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: JSON files
- **Server**: Flask development server

## Project Structure

```
academic-assessment-system/
│
├── app.py                  # Flask backend application
├── templates/
│   └── index.html         # Single-page frontend interface
├── users.json             # User accounts storage
├── records.json           # Exam records storage
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── testing/
│   ├── test_cases.md     # Test case documentation
│   ├── sample_input.json # Sample test data
│   └── sample_output.json# Expected output data
└── screenshots/          # Application screenshots
    ├── 01_login.png
    ├── 02_registration.png
    ├── 03_dashboard.png
    ├── 04_exam_entry.png
    └── 05_analysis.png
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/academic-assessment-system.git
cd academic-assessment-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Access the application**
Open your browser and navigate to: `http://127.0.0.1:5000`

## Usage

### 1. Registration
- Click "Register New Account" button
- Enter full name, username, and password
- Click "Register" to create account

### 2. Login
- Enter your username and password
- Click "Login" to access dashboard

### 3. Enter Exam Data
- Click "Enter Exam Data" button
- Fill in exam details (department, year, internal assessment, subject, date)
- Enter number of students
- Click "Generate Student Fields"
- Enter roll number, name, and marks for each student
- Leave marks blank for absent students
- Click "Submit & Analyze"

### 4. View Analysis
- View statistics: total, present, absent, highest, lowest, average
- See ranked student list with color-coded performance indicators
- Click "Back to Dashboard" to enter more data

## Testing

Comprehensive testing documentation is available in the `testing/` folder:

- **test_cases.md**: Detailed test cases with expected results
- **sample_input.json**: Sample input data for testing
- **sample_output.json**: Expected output for validation
- **screenshots/**: Visual proof of functionality

### Running Tests

1. Start the application: `python app.py`
2. Follow test cases in `testing/test_cases.md`
3. Compare results with expected outputs in `testing/sample_output.json`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve main HTML page |
| `/register` | POST | Register new user |
| `/login` | POST | Authenticate user |
| `/logout` | POST | Clear user session |
| `/save_exam` | POST | Save exam data and get analysis |
| `/get_records` | GET | Retrieve all exam records |
| `/filter_records` | POST | Filter records by criteria |
| `/get_alerts` | GET | Get performance alerts |

## Data Models

### User Object
```json
{
  "username": {
    "password": "string",
    "name": "string"
  }
}
```

### Exam Record Object
```json
{
  "department": "string",
  "year": "string",
  "internal": "string",
  "subject": "string",
  "date": "YYYY-MM-DD",
  "students": [
    {
      "roll": "string",
      "name": "string",
      "marks": "number or empty string"
    }
  ],
  "analysis": {
    "total": "number",
    "present": "number",
    "absent": "number",
    "highest": "number",
    "lowest": "number",
    "average": "number"
  },
  "ranked": [
    {
      "roll": "string",
      "name": "string",
      "marks": "number",
      "category": "high|average|low"
    }
  ]
}
```

## Performance Categorization Logic

- **High Performer**: Marks ≥ (Class Average + 10)
- **Average Performer**: (Class Average - 10) < Marks < (Class Average + 10)
- **Needs Attention**: Marks ≤ (Class Average - 10)

## Security Notes

⚠️ **Important**: This is a development version. For production use:
- Implement password hashing (bcrypt)
- Use environment variables for secret keys
- Add HTTPS/SSL encryption
- Implement CSRF protection
- Add input validation and sanitization
- Use a production WSGI server (Gunicorn, uWSGI)
- Use a proper database (PostgreSQL, MySQL)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Your Name - [Your GitHub Profile](https://github.com/yourusername)

## Acknowledgments

- Flask documentation
- Academic assessment best practices
- Educational technology research

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Note**: Screenshots and testing proof are included in the repository for verification purposes.
