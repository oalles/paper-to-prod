import os
import shutil
import argparse
from datetime import datetime, timedelta

def clean_sessions(base_dir="sessions", days=7, dry_run=False):
    now = datetime.now()
    if not os.path.exists(base_dir):
        print(f"No existe la carpeta {base_dir}. Nada que limpiar.")
        return
    for session in os.listdir(base_dir):
        session_path = os.path.join(base_dir, session)
        if not os.path.isdir(session_path):
            continue
        # Extraer fecha del nombre de la sesión si es posible
        try:
            date_str = session.split("_")[0]
            session_date = datetime.strptime(date_str, "%Y%m%d")
        except Exception:
            # Si no se puede parsear, usar fecha de modificación
            session_date = datetime.fromtimestamp(os.path.getmtime(session_path))
        if (now - session_date).days >= days:
            print(f"{'[DRY RUN] ' if dry_run else ''}Eliminando sesión: {session_path}")
            if not dry_run:
                shutil.rmtree(session_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Limpia workspaces de sesiones antiguas.")
    parser.add_argument("--days", type=int, default=7, help="Antigüedad mínima en días para eliminar (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Solo mostrar qué se eliminaría, sin borrar nada")
    parser.add_argument("--base-dir", type=str, default="sessions", help="Directorio base de sesiones")
    args = parser.parse_args()
    clean_sessions(base_dir=args.base_dir, days=args.days, dry_run=args.dry_run)
