# Odoo Addons — EAAI / Managua International Airport

A collection of **9 custom Odoo modules** (versions 13.0–15.0) developed for the **Empresa Administradora de Aeropuertos Internacionales (EAAI)** and **Managua International Airport (MNMG)**.

This suite provides an integrated **IT Service Management (ITIL)** and airport operations system, covering technical inventory, incident management, maintenance, network monitoring, telephony, flight plan billing, staff scheduling, and more.

---

## Modules

| Module | Version | Category | Description |
|--------|---------|----------|-------------|
| [`cmdb`](#cmdb) | 13.0 | ITIL / Technical Inventory | CMDB — Configuration management database for assets, services, locations, and technical staff. **Core module** depended on by most others. |
| [`ope_mgmt`](#ope_mgmt) | 13.0 | ITIL / Operations | Incident, change, and interruption management for equipment and services. |
| [`maint`](#maint) | 13.0 | Maintenance | Preventive maintenance plans and task scheduling for equipment. |
| [`net`](#net) | 13.0 | Network / Monitoring | Resource monitoring (CPU, memory, disk, network, processes) for servers and network devices. Includes a real-time chart dashboard. |
| [`sched`](#sched) | 13.0 | Scheduling | Shift rotation matrix and work schedule management for technical staff. Includes shift change requests and leave management. |
| [`atc_billing`](#atc_billing) | 13.0 | ATC / Billing | Flight plan recording for air navigation services billing. |
| [`pbx`](#pbx) | 14.0 | Telephony | Telephone extension and structured cabling point management with physical hierarchy (campus → building → room → rack → slot). |
| [`provet`](#provet) | 15.0 | Veterinary | Customization for *Productos Veterinarios de Nicaragua* (Provetnicsa): municipalities, default country (Nicaragua), and custom invoice format. |
| [`website_misc`](#website_misc) | 14.0 | Website | Minor utilities: hides the Odoo branding footer from the website. |

---

## Dependency Graph

```
                    base
                   /    \
                 mail    website
                /   \       \
              cmdb   project  website_misc
             / | \      |
           /   |  \     pbx
         /     |    \
    maint    net    ope_mgmt
       |
      sched

    atc_billing  (base only)
    provet       (base + account + sale_management)
```

External Python dependency: `holidays` (used by `net` and `sched` for Nicaragua holiday detection).

---

## Module Details

### `cmdb` — Configuration Management Database

The core module that models the organization's entire technical inventory:

- **Locations**: Buildings, offices
- **Systems & Subsystems**: SDD, FDD, RDCU, DLS, SNET, GW1, GW2, etc. (reflects airport communications and radar systems)
- **Manufacturers & Models**: Equipment brand and model catalog
- **Assets**: Physical inventory with serial number, location, owner, status (Good/Degraded/Failed/InStorage/Retired)
- **CI (Configuration Items)**: Items with ITMxxxx codes, linked to assets, systems, and subsystems
- **Services**: IT and communications services with SRVxxxx codes (AFTN, AIDC, radio frequencies, CENAMER, etc.)
- **Technicians**: Technical staff with digital signatures (inherits `res.partner`)
- **Customers**: User positions and serviced personnel

### `ope_mgmt` — Operational Management (Incidents)

ITIL-style incident management:

- Events with unique codes and tracking notes
- Incidents with code, report medium (Phone/Email/InPerson/SMS), source (Internal/External/Unknown), state (Draft → Open → InProgress → Cancelled → Closed)
- Relations to affected items, services, and customers
- Close wizard with closing comments
- *Stubs* for upcoming changes and interruptions modules

### `maint` — Maintenance

Preventive maintenance planning:

- Frequency catalog (with days) and status catalog
- Maintenance definitions linked to CMDB items
- Maintenance plans with scheduled programs
- Execution tracking: expected date, start, finish, responsible, support staff

### `net` — Network Monitoring

Server and network equipment monitoring via external agent:

- **Hosts**: IP, hostname, type (Server/Workstation), OS (Linux/Windows), associated system (AC/SDC/Radar)
- **Real-time metrics**: CPU (user, kernel, I/O wait, load), memory (total, free, available, buffers, cache), storage (disks, usage %), network interfaces (octets, errors), processes
- **Dashboard**: QWeb views with line charts for resource evolution
- Data populated by an external script writing to the Odoo database

### `sched` — Work Schedule Management

Complete shift rotation system for Radar Station staff:

- **Shift matrix**: Templates with 7-day cycles, each day assigned a shift (with hours)
- **Rolls**: Monthly schedule generation from a template, start date, and duration in weeks
- **Reports**: Monthly schedule in PDF/HTML with shift codes, total hours, and overtime. Landscape format, includes Nicaragua holidays.
- **Requests**: Shift changes (with digital signatures) and leave/vacation requests
- Integrates with `cmdb.technician` as employees

### `atc_billing` — ATC Flight Plan Billing

Flight plan recording for air navigation services charges:

- Call sign, registration, flight type (Scheduled/Unscheduled/General Aviation/Military/Other)
- Origin, destination, aircraft type
- UTC and local times: initial, takeoff, landing
- Includes external `fp_monitor.py` script using `odoorpc`

### `pbx` — PBX Telephony Management

Complete telephone infrastructure management with physical hierarchy:

- **Campus → Building → Room → Rack → Slot**: Auto-generated hierarchical codes (e.g., `MGA-TOR-A1-R01-E01`)
- **Numbers**: Extensions, virtual and direct numbers; type (Analog/Digital/IP); outbound permissions; capture groups
- **Points**: Structured cabling with origin and destination
- **Phonebook**: Institutional directory linked to contacts, areas, and positions
- **PDF Reports**: Cabling points organized by rack
- Integration with `project.task` for work orders (with duration in days/weeks)

### `provet` — Productos Veterinarios de Nicaragua (Veterinary Products)

Customization for Provetnicsa:

- Municipality catalog linked to states/departments of Nicaragua
- Default country: Nicaragua
- Tax ID field (`doc_id`) on contacts
- Custom invoice report format

### `website_misc` — Website Utilities

- Hides "Powered by Odoo" branding from the website footer

---

## Security

The security model is **role-based** with modular and cross-module groups:

| Group | Module | Scope |
|-------|--------|-------|
| `cmdb.root_group` (Technical Admin) | cmdb | Full CRUD on all models |
| `cmdb.technician_group` (Radar Technician) | cmdb | Read-only on most models |
| `cmdb.admin_technician_group` | net, ope_mgmt, maint, sched | Full CRUD (cross-module reference) |
| `billing_manager` | atc_billing | Full CRUD on flight plans |
| `billing_operator` | atc_billing | Read/create only |
| `pbx_admin_group` | pbx | Full CRUD on telephony |
| `pbx_tec_group` | pbx | CRUD (no delete) on numbers and points |
| `provet_ges_group` | provet | CRUD on municipalities |

---

## Installation

1. Clone the repository into your Odoo `addons` directory (or add the path to `--addons-path`):

```bash
git clone https://github.com/edxavier/odoo_addons.git
```

2. Install Python dependencies:

```bash
pip install holidays
```

3. Enable developer mode in Odoo and update the module list (`Apps → Update Apps List`).

4. Install the desired modules. It is recommended to install `cmdb` first since it is the foundation for most others.

5. For `net`, monitoring data is written by an external agent. For `atc_billing`, the `fp_monitor.py` script uses `odoorpc`.

---

## Technical Notes

- **Language**: The entire project is in Spanish (models, fields, views, reports, commit messages)
- **Odoo versions**: Most modules target 13.0. `pbx` and `website_misc` target 14.0. `provet` targets 15.0. Migration is required if running all modules on the same instance.
- **Core module**: `cmdb` is the central dependency — 5 modules depend on it directly.
- **Not yet implemented**: `ope_mgmt` has empty stubs for changes (`ope.changes`) and interruptions (`ope.interruptions`).

---

## Author

**Eder Xavier Rojas** — [@edxavier](https://github.com/edxavier)

Developed for the Empresa Administradora de Aeropuertos Internacionales (EAAI) — Managua International Airport, Nicaragua.
