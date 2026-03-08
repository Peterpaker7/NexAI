"""
NexAI Wearable Simulator
Simulates an AI wearable device sending patient vitals automatically
"""

import time
import random
import requests
import json
from datetime import datetime

# API endpoint
API_URL = "http://localhost:5000/predict"

# Patient profiles (you can simulate multiple patients)
PATIENTS = {
    "Jaya Keerthana": {
        "base_vitals": {
            "Age": 26,
            "SystolicBP": 145,
            "DiastolicBP": 92,
            "BS": 7.0,
            "BodyTemp": 98.0,
            "HeartRate": 80
        },
        "risk_type": "high"  # This patient has high risk
    },
    "Priya": {
        "base_vitals": {
            "Age": 28,
            "SystolicBP": 120,
            "DiastolicBP": 80,
            "BS": 6.0,
            "BodyTemp": 98.6,
            "HeartRate": 75
        },
        "risk_type": "low"  # This patient is healthy
    },
    "Lakshmi": {
        "base_vitals": {
            "Age": 35,
            "SystolicBP": 135,
            "DiastolicBP": 88,
            "BS": 8.5,
            "BodyTemp": 98.2,
            "HeartRate": 88
        },
        "risk_type": "mid"  # This patient has medium risk
    }
}

def add_realistic_variation(value, variation_percent=5):
    """Add small random variation to simulate real sensor readings"""
    variation = value * (variation_percent / 100)
    return value + random.uniform(-variation, variation)

def generate_vitals(patient_name):
    """Generate realistic vitals for a patient with small variations"""
    base = PATIENTS[patient_name]["base_vitals"]
    
    # Add small random variations to simulate real wearable readings
    vitals = {
        "Age": base["Age"],  # Age doesn't change
        "SystolicBP": round(add_realistic_variation(base["SystolicBP"], 3)),
        "DiastolicBP": round(add_realistic_variation(base["DiastolicBP"], 3)),
        "BS": round(add_realistic_variation(base["BS"], 5), 1),
        "BodyTemp": round(add_realistic_variation(base["BodyTemp"], 1), 1),
        "HeartRate": round(add_realistic_variation(base["HeartRate"], 5))
    }
    
    return vitals

def send_to_api(patient_name, vitals):
    """Send vitals to Flask API"""
    try:
        response = requests.post(
            API_URL,
            json=vitals,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"❌ API Error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure Flask is running on port 5000!")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def display_reading(patient_name, vitals, prediction):
    """Display the reading in a nice format"""
    print("\n" + "="*70)
    print(f"📱 WEARABLE DEVICE: {patient_name}'s Smart Monitor")
    print(f"🕐 Time: {datetime.now().strftime('%I:%M:%S %p')}")
    print("="*70)
    
    print("\n📊 VITALS CAPTURED:")
    print(f"  • Blood Pressure: {vitals['SystolicBP']}/{vitals['DiastolicBP']} mmHg")
    print(f"  • Blood Sugar: {vitals['BS']} mmol/L")
    print(f"  • Body Temperature: {vitals['BodyTemp']}°F")
    print(f"  • Heart Rate: {vitals['HeartRate']} bpm")
    print(f"  • Age: {vitals['Age']} years")
    
    if prediction:
        risk = prediction['risk_level'].upper()
        confidence = prediction['confidence']
        
        # Color coding
        if risk == "HIGH RISK":
            icon = "🔴"
        elif risk == "MID RISK":
            icon = "🟡"
        else:
            icon = "🟢"
        
        print(f"\n🤖 AI ANALYSIS:")
        print(f"  {icon} Risk Level: {risk}")
        print(f"  📈 Confidence: {confidence}%")
        
        if prediction.get('subtags'):
            print(f"  ⚠️  Detected: {', '.join(prediction['subtags'])}")
        
        print(f"\n💡 Recommendation:")
        print(f"  {prediction.get('recommendation', 'Continue monitoring')}")
    
    print("\n" + "="*70)

def simulate_single_patient(patient_name, interval=10):
    """Simulate one patient's wearable sending data"""
    print(f"\n🔵 Starting simulation for {patient_name}...")
    print(f"📡 Sending vitals every {interval} seconds")
    print("Press Ctrl+C to stop\n")
    
    try:
        reading_count = 0
        while True:
            reading_count += 1
            
            # Generate vitals
            vitals = generate_vitals(patient_name)
            
            # Send to API
            prediction = send_to_api(patient_name, vitals)
            
            # Display
            display_reading(patient_name, vitals, prediction)
            
            # Wait before next reading
            print(f"\n⏳ Next reading in {interval} seconds... (Reading #{reading_count})")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n✅ Simulation stopped!")
        print(f"Total readings sent: {reading_count}")

def simulate_all_patients(interval=15):
    """Simulate all patients sending data in rotation"""
    print("\n🔵 Starting multi-patient simulation...")
    print(f"📡 Each patient sends vitals every {interval} seconds")
    print("Press Ctrl+C to stop\n")
    
    try:
        reading_count = 0
        patient_list = list(PATIENTS.keys())
        
        while True:
            for patient_name in patient_list:
                reading_count += 1
                
                # Generate vitals
                vitals = generate_vitals(patient_name)
                
                # Send to API
                prediction = send_to_api(patient_name, vitals)
                
                # Display
                display_reading(patient_name, vitals, prediction)
                
                # Small delay between patients
                time.sleep(3)
            
            print(f"\n⏳ Next round of readings in {interval} seconds...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n✅ Simulation stopped!")
        print(f"Total readings sent: {reading_count}")

def demo_mode():
    """Quick demo - sends one reading per patient"""
    print("\n🎬 DEMO MODE: Sending one reading per patient...\n")
    
    for patient_name in PATIENTS.keys():
        vitals = generate_vitals(patient_name)
        prediction = send_to_api(patient_name, vitals)
        display_reading(patient_name, vitals, prediction)
        time.sleep(2)
    
    print("\n✅ Demo complete!")

# ============================================
# MAIN MENU
# ============================================

def main():
    print("="*70)
    print("         🏥 NexAI WEARABLE SIMULATOR 🏥")
    print("="*70)
    print("\nChoose simulation mode:")
    print("\n1. 👤 Single Patient (Kavitha) - High Risk Patient")
    print("2. 👤 Single Patient (Priya) - Healthy Patient")
    print("3. 👤 Single Patient (Lakshmi) - Medium Risk Patient")
    print("4. 👥 All Patients - Rotating simulation")
    print("5. 🎬 Demo Mode - One reading per patient (for judges)")
    print("6. ❌ Exit")
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    if choice == "1":
        interval = int(input("Enter interval in seconds (default 10): ") or "10")
        simulate_single_patient("Kavitha", interval)
    elif choice == "2":
        interval = int(input("Enter interval in seconds (default 10): ") or "10")
        simulate_single_patient("Priya", interval)
    elif choice == "3":
        interval = int(input("Enter interval in seconds (default 10): ") or "10")
        simulate_single_patient("Lakshmi", interval)
    elif choice == "4":
        interval = int(input("Enter interval in seconds (default 15): ") or "15")
        simulate_all_patients(interval)
    elif choice == "5":
        demo_mode()
    elif choice == "6":
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice!")

if __name__ == "__main__":
    main()
