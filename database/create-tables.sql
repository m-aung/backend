-- Users table (stores pet owners, veterinarians, and other staff)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) NOT NULL,  -- e.g., 'owner', 'veterinarian', 'staff'
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pets table (stores pet details)
CREATE TABLE IF NOT EXISTS pets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(10),
    microchip_id VARCHAR(50),
    notes TEXT
);

-- Association table to support multiple pet owners per pet
CREATE TABLE IF NOT EXISTS pet_owners (
    pet_id INTEGER REFERENCES pets(id) ON DELETE CASCADE,
    owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (pet_id, owner_id)
);

-- Appointments table (records scheduled visits)
CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    pet_id INTEGER REFERENCES pets(id) ON DELETE CASCADE,
    vet_id INTEGER REFERENCES users(id),  -- assumes vet has role 'veterinarian'
    appointment_date TIMESTAMP NOT NULL,
    reason TEXT,
    status VARCHAR(50) DEFAULT 'scheduled',  -- e.g., scheduled, completed, cancelled
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Treatments table (logs treatments provided to a pet)
CREATE TABLE IF NOT EXISTS treatments (
    id SERIAL PRIMARY KEY,
    pet_id INTEGER REFERENCES pets(id) ON DELETE CASCADE,
    appointment_id INTEGER REFERENCES appointments(id),
    treatment_date DATE NOT NULL,
    treatment_type VARCHAR(100),  -- e.g., surgery, therapy, etc.
    description TEXT,
    performed_by INTEGER REFERENCES users(id),  -- vet or technician
    notes TEXT
);

-- Vaccinations table (tracks vaccination records)
CREATE TABLE IF NOT EXISTS vaccinations (
    id SERIAL PRIMARY KEY,
    pet_id INTEGER REFERENCES pets(id) ON DELETE CASCADE,
    vaccine_name VARCHAR(100) NOT NULL,
    vaccination_date DATE NOT NULL,
    next_due_date DATE,
    administered_by INTEGER REFERENCES users(id),
    notes TEXT
);

-- Prescriptions table (stores prescription details)
CREATE TABLE IF NOT EXISTS prescriptions (
    id SERIAL PRIMARY KEY,
    pet_id INTEGER REFERENCES pets(id) ON DELETE CASCADE,
    appointment_id INTEGER REFERENCES appointments(id),
    medication VARCHAR(100) NOT NULL,
    dosage VARCHAR(50),
    frequency VARCHAR(50),
    duration VARCHAR(50),
    instructions TEXT,
    prescribed_date DATE DEFAULT CURRENT_DATE
);

-- Lab Tests table (records lab test information)
CREATE TABLE IF NOT EXISTS lab_tests (
    id SERIAL PRIMARY KEY,
    pet_id INTEGER REFERENCES pets(id) ON DELETE CASCADE,
    appointment_id INTEGER REFERENCES appointments(id),
    test_type VARCHAR(100),
    test_date DATE NOT NULL,
    results TEXT,
    performed_by INTEGER REFERENCES users(id),
    notes TEXT
);

-- Allergies table (tracks pet allergies)
CREATE TABLE IF NOT EXISTS allergies (
    id SERIAL PRIMARY KEY,
    pet_id INTEGER REFERENCES pets(id) ON DELETE CASCADE,
    allergen VARCHAR(100) NOT NULL,
    reaction TEXT,
    severity VARCHAR(50),  -- e.g., mild, moderate, severe
    notes TEXT
);
