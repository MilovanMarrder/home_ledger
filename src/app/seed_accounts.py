from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Account, AccountType

COA = [
    # ---- ASSETS (1xxx) ----
    ("1.1.01", "Efectivo", AccountType.ASSET),
    ("1.1.02", "Banco - Cuenta Principal", AccountType.ASSET),
    ("1.1.03", "Banco - Cuenta Secundaria", AccountType.ASSET),
    ("1.1.04", "Ahorros - Fondo Emergencia", AccountType.ASSET),
    ("1.1.05", "Ahorros - Metas", AccountType.ASSET),
    ("1.2.01", "CxC - Préstamos a familiares/amigos", AccountType.ASSET),
    ("1.2.02", "CxC - Reembolsos pendientes", AccountType.ASSET),
    ("1.3.01", "Inversiones - Fondos/ETFs", AccountType.ASSET),
    ("1.3.02", "Inversiones - Otros", AccountType.ASSET),

    # ---- LIABILITIES (2xxx) ----
    ("2.1.01", "Tarjeta de Crédito - BAC", AccountType.LIABILITY),
    ("2.1.02", "Tarjeta de Crédito - Ficohsa", AccountType.LIABILITY),
    ("2.1.03", "CxP - Servicios por pagar", AccountType.LIABILITY),
    ("2.1.04", "CxP - Otros", AccountType.LIABILITY),
    ("2.2.01", "Préstamo personal (banco)", AccountType.LIABILITY),
    ("2.2.02", "Préstamo vehículo", AccountType.LIABILITY),
    ("2.2.03", "Hipoteca", AccountType.LIABILITY),
    ("2.2.04", "Préstamos familiares", AccountType.LIABILITY),

    # ---- EQUITY (3xxx) ----
    ("3.1.01", "Capital personal / Aportes", AccountType.EQUITY),
    ("3.2.01", "Resultados acumulados", AccountType.EQUITY),

    # ---- INCOME (4xxx) ----
    ("4.1.01", "Salario", AccountType.INCOME),
    ("4.1.02", "Honorarios / Consultorías", AccountType.INCOME),
    ("4.1.03", "Ingresos financieros (intereses)", AccountType.INCOME),
    ("4.1.04", "Otros ingresos", AccountType.INCOME),
    ("4.1.05", "Reembolsos", AccountType.INCOME),

    # ---- EXPENSES (5xxx) ----
    ("5.1.01", "Vivienda - Renta / Hipoteca", AccountType.EXPENSE),
    ("5.1.02", "Vivienda - Electricidad", AccountType.EXPENSE),
    ("5.1.03", "Vivienda - Agua", AccountType.EXPENSE),
    ("5.1.04", "Vivienda - Internet/Telefonía", AccountType.EXPENSE),
    ("5.1.05", "Vivienda - Mantenimiento hogar", AccountType.EXPENSE),

    ("5.2.01", "Alimentación - Supermercado", AccountType.EXPENSE),
    ("5.2.02", "Alimentación - Restaurantes", AccountType.EXPENSE),

    ("5.3.01", "Transporte - Combustible", AccountType.EXPENSE),
    ("5.3.02", "Transporte - Mantenimiento vehículo", AccountType.EXPENSE),
    ("5.3.03", "Transporte - Movilidad", AccountType.EXPENSE),

    ("5.4.01", "Salud - Medicinas", AccountType.EXPENSE),
    ("5.4.02", "Salud - Consultas/Exámenes", AccountType.EXPENSE),
    ("5.4.03", "Salud - Seguros médicos", AccountType.EXPENSE),

    ("5.5.01", "Educación - Matrícula/Cuotas", AccountType.EXPENSE),
    ("5.5.02", "Educación - Libros/Cursos", AccountType.EXPENSE),

    ("5.6.01", "Finanzas - Comisiones bancarias", AccountType.EXPENSE),
    ("5.6.02", "Finanzas - Intereses", AccountType.EXPENSE),
    ("5.6.03", "Finanzas - Seguros", AccountType.EXPENSE),

    ("5.7.01", "Personal - Ropa", AccountType.EXPENSE),
    ("5.7.02", "Personal - Cuidado personal", AccountType.EXPENSE),
    ("5.7.03", "Personal - Suscripciones", AccountType.EXPENSE),

    ("5.8.01", "Ocio - Entretenimiento", AccountType.EXPENSE),
    ("5.8.02", "Social - Regalos/Donaciones", AccountType.EXPENSE),

    ("5.9.01", "Impuestos - Impuestos personales", AccountType.EXPENSE),
    ("5.9.02", "Impuestos - Tasas/multas", AccountType.EXPENSE),

    ("5.10.01", "Misceláneos - Imprevistos", AccountType.EXPENSE),
]

def main():
    db: Session = SessionLocal()
    try:
        for code, name, t in COA:
            exists = db.query(Account).filter(Account.code == code).one_or_none()
            if not exists:
                db.add(Account(code=code, name=name, type=t, is_active=True))
        db.commit()
        print("COA seeded.")
    finally:
        db.close()

if __name__ == "__main__":
    main()

