# 1️⃣ Imports
from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import os
from dotenv import load_dotenv
import groq
import json

# Load environment variables
load_dotenv()

# Configure Groq
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME', 'meta-llama/Llama-3-70b-chat-hf')

# Initialize Groq client
try:
    client = groq.Client(api_key=GROQ_API_KEY)
    print(f"Connected to Groq API with model: {MODEL_NAME}")
except Exception as e:
    print(f"Error initializing Groq client: {str(e)}")
    print("Please check your GROQ_API_KEY in the .env file")
    client = None

# Initialize Flask app
app = Flask(__name__)

def query_groq(prompt, max_tokens=200, temperature=0.7, top_p=0.9):
    """Send request to the Groq API and return the response."""
    if not client:
        print("Error: Groq client not initialized")
        return None
        
    try:
        print("\n--- Sending request to Groq API ---")
        print(f"Model: {MODEL_NAME}")
        print(f"Prompt: {prompt[:200]}..." if len(str(prompt)) > 200 else f"Prompt: {prompt}")
        
        # Make the API request
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": str(prompt)
                }
            ],
            model=MODEL_NAME,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False
        )
        
        # Extract the response
        if hasattr(chat_completion, 'choices') and chat_completion.choices:
            response = chat_completion.choices[0].message.content
            print(f"\n--- Response from Groq API ---")
            print(f"Response: {response}")
            return response
        else:
            print("Error: Unexpected response format from Groq API")
            return None
            
    except Exception as e:
        error_msg = f"\n--- Error in query_groq ---\n{str(e)}"
        import traceback
        error_msg += "\n" + traceback.format_exc()
        print(error_msg)
        return None

def generate_offer_message(row):
    """Generate a personalized offer message using Groq API with structured offer rules."""
    try:
        # Extract customer data
        name = row['customer_name']
        last_service = row['last_service']
        visits = int(row.get('visits', 1))
        days_since_visit = int(row.get('days_since_last_visit', 0))
        
        # Define service combinations
        service_combos = {
            'Haircut': ['Hair Spa', 'Hair Color', 'Blow Dry'],
            'Facial': ['Face Massage', 'Clean Up', 'Bleach'],
            'Manicure': ['Pedicure', 'Nail Art', 'Hand Spa'],
            'Pedicure': ['Manicure', 'Foot Spa', 'Nail Polish'],
            'Hair Spa': ['Haircut', 'Hair Treatment', 'Head Massage'],
            'Body Massage': ['Body Scrub', 'Steam Bath', 'Aromatherapy']
        }
        
        # Get complementary services
        complementary_services = service_combos.get(last_service, ['Hair Spa', 'Facial', 'Manicure'])
        
        # Determine offer type based on visits and days since last visit
        if days_since_visit > 30:  # Win-back offer
            offer_type = "We Missed You Special"
            discount = "35%"
            combo = f"{last_service} + {complementary_services[0]}"
            extra = "with a free hair spa session"
            emoji = "💫"
            visit_context = f"It's been {days_since_visit} days since your last {last_service} visit — we've missed you!"
        elif visits >= 5:  # VIP
            offer_type = "VIP Treatment"
            discount = "35%"
            combo = f"{last_service} + {complementary_services[0]}"
            extra = "plus a free head massage"
            emoji = "👑"
            if days_since_visit > 20:
                visit_context = f"It's been {days_since_visit} days since your last visit — your perfect self-care moment awaits!"
            else:
                visit_context = f"As one of our valued VIPs, you deserve something special!"
        elif visits >= 3:  # Regular
            offer_type = "Special Offer"
            discount = "30%"
            combo = f"{last_service} + {complementary_services[0]}"
            extra = "plus a free nail art"
            emoji = "💎"
            if days_since_visit > 20:
                visit_context = f"It's been {days_since_visit} days since your last visit — time to treat yourself!"
            else:
                visit_context = f"We love having you back for your {visits}th visit!"
        elif visits == 2:  # Returning
            offer_type = "Welcome Back"
            discount = "25%"
            combo = f"{last_service} + {complementary_services[0]}"
            extra = ""
            emoji = "💖"
            if days_since_visit > 20:
                visit_context = f"It's been {days_since_visit} days since your last visit — we've missed you!"
            else:
                visit_context = f"We're so happy to see you back for your second visit!"
        else:  # New
            offer_type = "New Customer"
            discount = "20%"
            combo = last_service
            extra = "plus a free 15-minute consultation"
            emoji = "👋"
            visit_context = "We're excited to have you try our services for the first time!"
        
        # Create the system prompt with the offer rules
        system_prompt = """You are a creative salon marketing assistant. Follow these rules for offers:

1. CUSTOMER TIERS:
   - New (1 visit): 20% off first service
   - Returning (2 visits): 25% off
   - Regular (3-4 visits): 30% off
   - VIP (5+ visits): 35% off
   - Inactive (>30 days): 35% off "We Missed You" special

2. MESSAGE FORMAT:
   - Start with "Hi [Name]! [Emoji]"
   - Include offer type (VIP TREATMENT, SPECIAL OFFER, etc.)
   - List the service combo
   - Show discount
   - Add extra benefit
   - End with a call-to-action

3. EMOJIS:
   - VIP: 👑
   - Special: 💎
   - Welcome: 👋
   - Win-back: 💫
   - Returning: 💖
   - General: 💇‍♀️✨
"""

        # Create the user prompt with customer data
        user_prompt = f"""Create a personalized salon offer with these details:
- Customer: {name}
- Last Service: {last_service}
- Visits: {visits}
- Days Since Last Visit: {days_since_visit}
- Context: {visit_context}
- Offer Type: {offer_type}
- Combo: {combo}
- Discount: {discount}
- Extra: {extra}
- Emoji: {emoji}

Generate a friendly, 1-2 sentence offer that:
1. References their visit history or last visit
2. Feels personal and warm
3. Includes the offer details naturally
4. Uses 1-2 emojis

Example: "Hi [Name]! It's been [X] days since your last [Service] — we've missed you! Enjoy [Discount] off your next visit, plus [Extra]! [Emoji]"
"""

        # Generate the offer using Groq API
        if client:
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model=MODEL_NAME,
                    temperature=0.7,
                    max_tokens=100,
                    top_p=0.9
                )
                
                if chat_completion.choices and chat_completion.choices[0].message.content:
                    ai_response = chat_completion.choices[0].message.content.strip()
                    # Ensure the response starts with the customer's name
                    if not (ai_response.startswith(f"Hi {name}") or ai_response.startswith(name)):
                        ai_response = f"Hi {name}! {ai_response}"
                    return ai_response
                    
            except Exception as e:
                print(f"AI generation failed: {str(e)}")
        
        # Fallback to template-based message
        if visits >= 5:
            if days_since_visit > 20:
                return f"Hi {name}! {emoji} It's been {days_since_visit} days since your last visit — your perfect self-care moment awaits! Enjoy {discount} off {combo} {extra}. {emoji}"
            else:
                return f"Hi {name}! {emoji} As one of our valued VIPs, you deserve something special! Enjoy {discount} off {combo} {extra}. {emoji}"
        elif visits >= 3:
            if days_since_visit > 20:
                return f"Hi {name}! {emoji} It's been {days_since_visit} days since your last visit — time to treat yourself! Enjoy {discount} off {combo} {extra}. {emoji}"
            else:
                return f"Hi {name}! {emoji} We love having you back for your {visits}th visit! Enjoy {discount} off {combo} {extra}. {emoji}"
        elif visits == 2:
            if days_since_visit > 20:
                return f"Hi {name}! {emoji} It's been {days_since_visit} days since your last visit — we've missed you! Enjoy {discount} off {combo} {extra}. {emoji}"
            else:
                return f"Hi {name}! {emoji} Welcome back for your second visit! Enjoy {discount} off {combo} {extra}. {emoji}"
        else:
            return f"Hi {name}! {emoji} We're excited to have you try our {last_service} for the first time! Enjoy {discount} off plus a free 15-minute consultation. {emoji}"
            
    except Exception as e:
        print(f"Error in generate_offer_message: {str(e)}")
        # Final fallback - only return if not within 20 days
        if 'days_since_visit' in locals() and days_since_visit <= 20:
            return None
        return f"Hi {row.get('customer_name', 'there')}! We have a special offer on {row.get('last_service', 'our services')} just for you! 💇‍♀️"

# HTML Template for the web interface
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Salon Offers Generator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 8px; }
        .result { margin-top: 20px; padding: 15px; background: #fff; border-radius: 4px; }
        .offer { margin: 10px 0; padding: 10px; border-left: 4px solid #4CAF50; }
        .error { color: #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Salon Offers Generator</h1>
        <form method="post" enctype="multipart/form-data" action="/generate_offers">
            <input type="file" name="file" accept=".csv" required>
            <button type="submit">Generate Offers</button>
        </form>
        
        {% if results %}
        <div class="result">
            <h2>Generated Offers</h2>
            {% for result in results %}
                <div class="offer">
                    <strong>{{ result.customer_name }}</strong>: {{ result.offer_message }}
                </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if error %}
        <div class="error">
            <strong>Error:</strong> {{ error }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Root route to display the form
@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

# 5️⃣ Flask endpoint for form submission
@app.route('/generate_offers', methods=['GET', 'POST'])
def generate_offers():
    if 'file' not in request.files:
        if request.accept_mimetypes.accept_json:
            return jsonify({'error': 'No file part'}), 400
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        if request.accept_mimetypes.accept_json:
            return jsonify({'error': 'No selected file'}), 400
        return "No selected file", 400
    
    if file and file.filename.endswith('.csv'):
        try:
            # Read the CSV file
            df = pd.read_csv(file)
            
            # Generate offers for each customer
            offers = []
            for _, row in df.iterrows():
                offer = generate_offer_message(row)
                offers.append({
                    'customer_name': row['customer_name'],
                    'offer': offer,
                    'last_service': row['last_service']
                })
            
            # Print JSON output in terminal for debugging
            print("Generated offers:", offers)
            
            # Return JSON for API requests, HTML for web requests
            if request.accept_mimetypes.accept_json:
                return jsonify(offers)
            return render_template_string(HTML_TEMPLATE, results=offers)
            
        except Exception as e:
            error_msg = f"Error processing file: {str(e)}"
            if request.accept_mimetypes.accept_json:
                return jsonify({'error': error_msg}), 500
            return error_msg, 500
    
    error_msg = "Invalid file format. Please upload a CSV file."
    if request.accept_mimetypes.accept_json:
        return jsonify({'error': error_msg}), 400
    return error_msg, 400

# 6️⃣ Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
