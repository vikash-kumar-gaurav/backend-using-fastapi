from dotenv import load_dotenv
import os
load_dotenv()
def verificationLink_onRegister(email,token):
    verification_link_base = os.getenv("VERIFICATION_ROUTES")
    if not verification_link_base:
        raise ValueError("VERIFICATION_ROUTES is not set in environment variables")

    verification_link = f"{verification_link_base}{token}"
    html = f"""
        <div style="font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f4f4f4; padding: 30px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;">

            <h2 style="color: #000000; text-align: center; margin-bottom: 25px;">🎓 Welcome to Education University Center</h2>

            <p style="font-size: 16px; color: #333333;">
            Hi <strong>{email}</strong>,
            <br><br>
            We're happy to have you here. Your journey with us starts now — but first, we just need to confirm that this is really you.
            <br><br>
            Please click the button below to verify your email address.
            </p>

            <div style="text-align: center; margin: 35px 0;">
            <a href="{verification_link}" style="background-color: #000000; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-size: 16px; font-weight: bold;">
                Verify Your Email
            </a>
            </div>

            <p style="font-size: 15px; color: #555555;">
            If you didn’t sign up with us, no worries — you can simply ignore this message.
            </p>

            <div style="margin-top: 40px; padding: 16px; background-color: #fafafa; border-left: 4px solid #000000;">
            <p style="font-size: 14px; color: #555555;">
                Need help? Reach out to us anytime at
                <a href="mailto:support@educationuniversitycenter.edu" style="color: #000000; text-decoration: underline;">
                support@educationuniversitycenter.edu
                </a>
            </p>
            </div>

            <hr style="margin: 40px 0; border: none; border-top: 1px solid #ddd;">

            <p style="font-size: 12px; color: #999999; text-align: center;">
            © 2025 Education University Center. All rights reserved.
            </p>
        </div>
        </div>
        """


    return html