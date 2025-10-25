# Salon Offers Generator

An intelligent offer generation system for salons that creates personalized offers based on customer visit history using AI-powered natural language generation.

## 🌟 Features

- **AI-Powered Offers**: Uses Groq's LLaMA 3 70B model for natural-sounding, personalized offers
- **Smart Customer Segmentation**: Different offers for new, returning, regular, and VIP customers
- **Visit-Based Logic**: Tailors messages based on visit frequency and recency
- **Web Interface**: Simple HTML interface for easy interaction
- **RESTful API**: Can be integrated with other systems
- **Responsive Design**: Works on both desktop and mobile devices

## 🛠 Technologies Used

- **Backend**: Python 3.8+
- **Web Framework**: Flask
- **AI/ML**: Groq API with LLaMA 3 70B model
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas
- **Environment Management**: python-dotenv

## 🚀 End-to-End Flow

1. **User Input**: Customer data is provided via the web form or API
2. **Data Processing**: System processes visit history and service preferences
3. **Offer Generation**: AI generates a personalized offer based on business rules
4. **Response Delivery**: Formatted offer is displayed in the web interface or returned via API
5. **User Action**: Customer can view and use the generated offer

## 🏗 Installation

1. Clone the repository:
   ```bash
   git clone [your-repository-url]
   cd salon-offers-generator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     MODEL_NAME=meta-llama/Llama-3-70b-chat-hf
     ```

## 🖥 Web Interface

The application includes a responsive web interface with the following features:

- **Input Form**: Simple form to enter customer details
- **Real-time Processing**: Instant offer generation
- **Clean UI**: Modern, user-friendly design
- **Responsive Layout**: Works on all device sizes

### Screenshot:

```
+---------------------------------------------+
|          SALON OFFERS GENERATOR            |
+---------------------------------------------+
|  Customer Name:  [_____________________]   |
|  Last Service:   [_____________________]   |
|  Total Visits:   [____]                    |
|  Days Since Last Visit: [____]             |
|                                            |
|  [ GENERATE OFFER ]                        |
|                                            |
|  Generated Offer:                          |
|  --------------------------------------   |
|  Hi [Name]! [Emoji] [Personalized Message] |
|  --------------------------------------   |
+---------------------------------------------+
```

## 📊 Offer Generation Logic

### Customer Segmentation

| Customer Type      | Visits | Days Since Last Visit | Offer Details |
|--------------------|--------|----------------------|---------------|
| New Customer      | 1      | Any                  | 20% off first service |
| Returning         | 2      | Any                  | 25% off + service combo |
| Regular           | 3-4    | Any                  | 30% off + free nail art |
| VIP               | 5+     | Any                  | 35% off + free head massage |
| Inactive          | Any    | >30 days             | 35% off + free hair spa |

### Message Generation Rules

1. **For recent visits (≤20 days)**:
   - Focus on visit count
   - Example: "We love having you back for your 3rd visit!"

2. **For less recent visits (>20 days)**:
   - Mention days since last visit
   - Example: "It's been 42 days since your last visit — we've missed you!"

3. **For inactive customers (>30 days)**:
   - Special win-back message
   - Higher value offer

## 🚀 Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## 🌐 API Endpoints

### Generate Offer
- **URL**: `/generate_offer`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "customer_name": "Riya",
    "last_service": "Hair Spa",
    "visits": 3,
    "days_since_last_visit": 45
  }
  ```
- **Success Response**:
  ```json
  {
    "customer_name": "Riya",
    "offer_message": "Hi Riya! 💎 It's been 45 days since your last visit — time to treat yourself! Enjoy 30% off Hair Spa + Haircut plus a free nail art. 💎"
  }
  ```

## 🧪 Example Scenarios

### Scenario 1: New Customer
```json
{
  "customer_name": "Aarav",
  "last_service": "Haircut",
  "visits": 1,
  "days_since_last_visit": 0
}
```
**Response**:
```json
{
  "customer_name": "Aarav",
  "offer_message": "Hi Aarav! 👋 We're excited to have you try our Haircut for the first time! Enjoy 20% off plus a free 15-minute consultation. 👋"
}
```

### Scenario 2: VIP Customer
```json
{
  "customer_name": "Priya",
  "last_service": "Hair Spa",
  "visits": 7,
  "days_since_last_visit": 15
}
```
**Response**:
```json
{
  "customer_name": "Priya",
  "offer_message": "Hi Priya! 👑 As one of our valued VIPs, you deserve something special! Enjoy 35% off Hair Spa + Haircut plus a free head massage. 👑"
}
```

## 🛠 Troubleshooting

### Common Issues

1. **API Key Not Found**
   - Ensure `.env` file exists in the root directory
   - Verify the API key is correctly set

2. **Server Not Starting**
   - Check if port 5000 is already in use
   - Verify all dependencies are installed

3. **AI Generation Fails**
   - Check internet connection
   - Verify Groq API key is valid and has sufficient credits


## 🙏 Acknowledgments

- Groq for the powerful LLaMA 3 70B model
- Flask for the lightweight web framework
- All open-source contributors
