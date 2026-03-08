# Home Ledger

Home Ledger es una herramienta personal para registrar, clasificar y analizar movimientos financieros del hogar a partir de interacciones conversacionales.

La idea principal es simple:

- un usuario envía un mensaje al bot de Telegram,
- el sistema interpreta el movimiento financiero,
- genera una **propuesta de registro**,
- solicita **confirmación o edición**,
- y solo después guarda el movimiento en la base de datos.

## Objetivo del proyecto

Construir una herramienta privada y evolutiva para la gestión financiera del hogar, con énfasis en:

- privacidad de la información,
- facilidad de captura desde Telegram,
- confirmación humana antes del registro final,
- base de datos estructurada,
- dashboards para apoyar decisiones financieras,
- posibilidad de crecer hacia voz, imagen y modelos locales.

## Problema que resuelve

Registrar finanzas personales suele fallar por fricción:

- abrir una app,
- elegir categoría,
- llenar campos,
- mantener disciplina.

Home Ledger reduce esa fricción permitiendo registrar movimientos con lenguaje natural, por ejemplo:

- `Compré leche y pan, 145 lempiras en efectivo`
- `Me pagaron 8500`
- `Transferí 2000 a la tarjeta`
- `Gasolina 900 en texaco`

El sistema transforma ese mensaje en una propuesta estructurada y pide confirmación antes de guardarlo.

## Alcance actual del MVP

### Incluye
- Bot de Telegram por polling
- Backend con FastAPI
- PostgreSQL
- Extracción estructurada desde texto
- Flujo de confirmación
- Flujo de edición simple
- Registro de transacciones confirmadas
- Base conceptual para doble partida contable

### No incluye todavía
- OCR robusto para facturas
- Procesamiento de voz
- Procesamiento de imagen
- Presupuestos avanzados
- Alertas inteligentes
- Disponibilidad 24/7 en servidor dedicado
- Modelo local

## Flujo del MVP

1. El usuario envía un mensaje de texto al bot.
2. El backend crea un `InboxItem`.
3. El sistema genera un `TransactionDraft`.
4. El bot responde con una propuesta legible:
   - tipo
   - monto
   - moneda
   - fecha
   - comercio
   - notas
   - categoría sugerida
5. El usuario responde:
   - `si`
   - `no`
   - `editar campo=valor`
6. Si confirma, se crea la transacción final y su asiento contable.
7. Si edita, se actualiza el draft y se vuelve a mostrar la propuesta.
8. Si rechaza, el draft queda cancelado.

## Filosofía del sistema

Home Ledger no usa el modelo de lenguaje para decidir de forma autónoma e irreversible.

La filosofía es:

- reglas y validaciones locales,
- el modelo propone,
- el usuario confirma,
- el sistema registra.

Esto reduce errores y mantiene el control humano sobre datos financieros sensibles.

## Arquitectura

### Componentes
- **Telegram Bot**: interfaz conversacional
- **FastAPI**: backend y lógica de negocio
- **PostgreSQL**: persistencia
- **OpenAI API**: extracción estructurada inicial
- **Alembic**: migraciones
- **SQLAlchemy**: ORM

### Flujo de datos
`Telegram message -> InboxItem -> TransactionDraft -> user confirmation -> Transaction -> JournalEntry`

## Modelo conceptual

### InboxItem
Representa la entrada cruda del usuario.

### TransactionDraft
Representa la interpretación preliminar del sistema.

### Transaction
Representa el movimiento confirmado.

### JournalEntry / JournalLine
Representan la estructura contable de doble partida.

## Estructura del proyecto

```text
home_ledger/
├─ alembic/
├─ src/
│  ├─ app/
│  │  ├─ api/
│  │  ├─ services/
│  │  ├─ config.py
│  │  ├─ db.py
│  │  ├─ main.py
│  │  ├─ models.py
│  │  └─ schemas.py
│  └─ telegram_bot/
│     ├─ bot.py
│     └─ client.py
├─ docker-compose.yml
├─ pyproject.toml
└─ README.md