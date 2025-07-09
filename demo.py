for var in ["batch", "email", "name", "gender", "yob", "mobile", "whatsapp", "hometowncity", "hometowndistrict", "hometownstate", "hometowncountry", "residencecity", "residencestate", "residentcountry", "residentzip", "education", "profession", "referrer_id", "status", "bio", "visa_type"]:
    print(f"""
            <p>
                {{ form.{var}.label }}<br>
                {{ form.{var}(size=32) }}<br>
                xxx
                <span style="color: red;">[{{ error }}]</span>
                yyy
            </p>""", end="")