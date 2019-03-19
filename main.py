import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


def to_float(flt):
    try:
        return float(flt)
    except ValueError:
        return 0.0


@app.route('/add_donation', methods=['GET', 'POST'])
def add_donation():
    if request.method == 'GET':
        # User clicked the "add donation" link to get here
        donors = Donor.select()
        return render_template('add_donation.jinja2', donors=donors)
    elif request.method == 'POST':
        # User pressed the 'add' button
        donor_name = Donor.select().where(Donor.name == request.form['name']).get()
        donation_amount = to_float(request.form['donation'])
        if donation_amount > 0.0:
            Donation(donor=donor_name, value=donation_amount).save()
        return redirect(url_for('all'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

