from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from .database import db, User, Input
from .models.emission_model import calculate_emissions, predict_future_emissions
from .models.visualizations import plot_emission_trend, plot_category_breakdown
import pandas as pd
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('main.register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password.', 'error')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.home'))

@bp.route('/input', methods=['GET', 'POST'])
@login_required
def input_data():
    if request.method == 'POST':
        energy = float(request.form['energy'])
        miles = float(request.form['miles'])
        waste = float(request.form['waste'])
        emissions = calculate_emissions(energy, miles, waste)
        new_input = Input(
            user_id=current_user.id,
            energy_kwh=energy,
            miles_driven=miles,
            waste_kg=waste,
            emissions=emissions
        )
        db.session.add(new_input)
        db.session.commit()
        flash('Data saved successfully.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('input.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    user_inputs = Input.query.filter_by(user_id=current_user.id).all()
    if not user_inputs:
        return render_template('dashboard.html', plot=None, breakdown=None, prediction=None)
    df = pd.DataFrame([{'date': i.date, 'emissions': i.emissions, 'energy_kwh': i.energy_kwh, 'miles_driven': i.miles_driven, 'waste_kg': i.waste_kg} for i in user_inputs])
    trend_plot = plot_emission_trend(df)
    latest = user_inputs[-1]
    breakdown_plot = plot_category_breakdown(latest.energy_kwh, latest.miles_driven, latest.waste_kg)
    prediction = predict_future_emissions(df.to_dict('records'))
    return render_template('dashboard.html', plot=trend_plot, breakdown=breakdown_plot, prediction=prediction)

@bp.route('/insights')
@login_required
def insights():
    user_inputs = Input.query.filter_by(user_id=current_user.id).all()
    recommendations = []
    if user_inputs:
        latest = user_inputs[-1]
        if latest.energy_kwh > 500:
            recommendations.append("Consider switching to energy-efficient appliances to reduce electricity usage.")
        if latest.miles_driven > 100:
            recommendations.append("Try carpooling or using public transport to lower travel emissions.")
        if latest.waste_kg > 10:
            recommendations.append("Increase recycling and composting to minimize waste emissions.")
    if not recommendations:
        recommendations.append("Great job! Keep maintaining low emissions.")
    return render_template('insights.html', recommendations=recommendations)