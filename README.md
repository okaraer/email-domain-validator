# 📧 Email Domain Validator


![banner](img_comp.png)


Validate email domains in an Excel file by checking DNS MX records.

If a domain has a valid mail server:

```
1 = Active
0 = Inactive
```

---

## 🐍 Install Python

If Python is not installed:

👉 https://www.python.org/downloads/

During installation:

✅ Check **"Add Python to PATH"**

Verify installation:

```
python --version
```

---

## 📦 Install Dependencies

```
pip install -r requirements.txt
```

---

## ▶ How to Run

Place your Excel file in the project folder.

Run:

```
python email_domain_validator.py --input sample_emails.xlsx --output result.xlsx
```

---

## 📁 Input Format

Excel must contain a column named:

```
email
```

Example:

| email |
|------|
| test@gmail.com |
| info@company.com |

---

## 📊 Output

A new column is added:

```
domain_active
```

| email | domain_active |
|------|---------------|
| gmail.com | 1 |
| fake-domain.xyz | 0 |

---

## ⚠ Limitations

This tool checks:

✔ Domain exists  
✔ MX record exists  

It does NOT guarantee mailbox deliverability.

---

## 📜 License

MIT License
