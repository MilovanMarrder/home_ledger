from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Category

CATEGORIES = [
    # ----- INCOME -----
    ("INC.SALARY", "Ingreso - Salario", "income", "Ingresos", "Salario", "1.1.02", "4.1.01", "salario,pago,nomina"),
    ("INC.CONSULT", "Ingreso - Consultorías", "income", "Ingresos", "Honorarios", "1.1.02", "4.1.02", "consultoria,honorarios,servicio"),
    ("INC.INTEREST", "Ingreso - Intereses", "income", "Ingresos", "Intereses", "1.1.02", "4.1.03", "interes,intereses"),
    ("INC.OTHER", "Ingreso - Otros", "income", "Ingresos", "Otros", "1.1.02", "4.1.04", "ingreso,otros"),

    # ----- EXPENSE: HOUSING -----
    ("EXP.HOME.RENT", "Vivienda - Renta/Hipoteca", "expense", "Vivienda", "Renta/Hipoteca", "5.1.01", "1.1.02", "renta,alquiler,hipoteca"),
    ("EXP.HOME.ELEC", "Vivienda - Electricidad", "expense", "Vivienda", "Electricidad", "5.1.02", "1.1.02", "eeh,energia,electricidad"),
    ("EXP.HOME.WATER", "Vivienda - Agua", "expense", "Vivienda", "Agua", "5.1.03", "1.1.02", "agua,sanasa"),
    ("EXP.HOME.INET", "Vivienda - Internet/Telefonía", "expense", "Vivienda", "Internet", "5.1.04", "1.1.02", "tigo,claro,internet,telefono"),
    ("EXP.HOME.MAINT", "Vivienda - Mantenimiento", "expense", "Vivienda", "Mantenimiento", "5.1.05", "1.1.02", "mantenimiento,arreglo,reparacion"),

    # ----- EXPENSE: FOOD -----
    ("EXP.FOOD.GROCERY", "Alimentación - Supermercado", "expense", "Alimentación", "Supermercado", "5.2.01", "1.1.02", "super,colonia,walmart,pricesmart,despensa"),
    ("EXP.FOOD.REST", "Alimentación - Restaurantes", "expense", "Alimentación", "Restaurantes", "5.2.02", "1.1.02", "restaurante,pizza,cafe,pollo,burger"),

    # ----- EXPENSE: TRANSPORT -----
    ("EXP.TRANS.FUEL", "Transporte - Combustible", "expense", "Transporte", "Combustible", "5.3.01", "1.1.02", "texaco,puma,shell,gasolina,combustible"),
    ("EXP.TRANS.MAINT", "Transporte - Mantenimiento", "expense", "Transporte", "Mantenimiento", "5.3.02", "1.1.02", "taller,llantas,aceite,mecanico"),
    ("EXP.TRANS.MOB", "Transporte - Movilidad", "expense", "Transporte", "Movilidad", "5.3.03", "1.1.02", "uber,indriver,taxi"),

    # ----- EXPENSE: HEALTH -----
    ("EXP.HEALTH.MEDS", "Salud - Medicinas", "expense", "Salud", "Medicinas", "5.4.01", "1.1.02", "farmacia,kielsa,puntofarma"),
    ("EXP.HEALTH.CONS", "Salud - Consultas/Exámenes", "expense", "Salud", "Consultas", "5.4.02", "1.1.02", "consulta,examen,clinica,hospital"),

    # ----- EXPENSE: EDUCATION -----
    ("EXP.EDU.TUITION", "Educación - Matrícula/Cuotas", "expense", "Educación", "Matrícula", "5.5.01", "1.1.02", "unah,matricula,cuota,colegiatura"),
    ("EXP.EDU.COURSE", "Educación - Cursos/Libros", "expense", "Educación", "Cursos", "5.5.02", "1.1.02", "curso,libro,udemy,coursera"),

    # ----- EXPENSE: FINANCE -----
    ("EXP.FIN.FEES", "Finanzas - Comisiones", "expense", "Finanzas", "Comisiones", "5.6.01", "1.1.02", "comision,fee,membresia,cargo"),
    ("EXP.FIN.INTEREST", "Finanzas - Intereses", "expense", "Finanzas", "Intereses", "5.6.02", "1.1.02", "interes,mora"),
    ("EXP.FIN.INSURANCE", "Finanzas - Seguros", "expense", "Finanzas", "Seguros", "5.6.03", "1.1.02", "seguro,poliza"),

    # ----- EXPENSE: PERSONAL -----
    ("EXP.PERS.CLOTH", "Personal - Ropa", "expense", "Personal", "Ropa", "5.7.01", "1.1.02", "ropa,zapatos"),
    ("EXP.PERS.CARE", "Personal - Cuidado personal", "expense", "Personal", "Cuidado", "5.7.02", "1.1.02", "barberia,estetica,shampoo"),
    ("EXP.PERS.SUBS", "Personal - Suscripciones", "expense", "Personal", "Suscripciones", "5.7.03", "1.1.02", "netflix,spotify,icloud,google"),

    # ----- EXPENSE: LEISURE -----
    ("EXP.LEIS.ENT", "Ocio - Entretenimiento", "expense", "Ocio", "Entretenimiento", "5.8.01", "1.1.02", "cine,entretenimiento"),
    ("EXP.LEIS.GIFT", "Social - Regalos/Donaciones", "expense", "Ocio", "Regalos", "5.8.02", "1.1.02", "regalo,donacion"),

    # ----- EXPENSE: TAX -----
    ("EXP.TAX", "Impuestos y tasas", "expense", "Impuestos", "Impuestos", "5.9.01", "1.1.02", "impuesto,tasa,multa"),

    # ----- EXPENSE: MISC -----
    ("EXP.MISC", "Misceláneos / Imprevistos", "expense", "Misceláneos", "Imprevistos", "5.10.01", "1.1.02", "imprevisto,otros"),
]

def main():
    db: Session = SessionLocal()
    try:
        for code, name, kind, group, subgroup, dr, cr, kw in CATEGORIES:
            exists = db.query(Category).filter(Category.code == code).one_or_none()
            if not exists:
                db.add(Category(
                    code=code,
                    name=name,
                    kind=kind,
                    group=group,
                    subgroup=subgroup,
                    default_debit_account_code=dr,
                    default_credit_account_code=cr,
                    keywords=kw,
                    is_active=True
                ))
        db.commit()
        print("Categories seeded.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
