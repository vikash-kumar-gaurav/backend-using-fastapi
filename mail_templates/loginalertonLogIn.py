def login_alert_html(name, location,time):
    formatted_time = time.strftime("%d %B %Y, %I:%M %p")  # Example: 10 April 2025, 04:15 PM

    return f"""
    <div style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: white; padding: 30px;
                    border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #2c3e50;">🔐 Login Alert - Education University Center</h2>
            <p style="font-size: 16px; color: #333;">
                Hello <b>{name}</b>,<br><br>
                A new login to your account was detected from the following location at <b>{formatted_time}</b>:
            </p>
            <ul style="font-size: 15px; color: #555; list-style: none; padding-left: 0;">
                <li><strong>🌍 City:</strong> {location["city"]}</li>
                <li><strong>🏙 Region:</strong> {location["region"]}</li>
                <li><strong>🇮🇳 Country:</strong> {location["country"]}</li>
            </ul>
            <p style="font-size: 14px; color: #999;">
                If this was you, no action is needed.<br>
                If you didn’t recognize this login, please contact support immediately.
            </p>
            <hr style="margin-top: 30px;">
            <p style="font-size: 12px; color: #aaa; text-align: center;">
                &copy; 2025 Education University Center. All rights reserved.
            </p>
        </div>
    </div>
    """
