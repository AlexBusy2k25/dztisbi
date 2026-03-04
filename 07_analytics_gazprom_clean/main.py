import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import random

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)


def create_sample_data():
    """Создаёт тестовые данные по скважинам"""

    wells_data = {
        'well_id': [f'СКВ-{i:03d}' for i in range(1, 11)],
        'debit_fact': [random.randint(80, 160) for _ in range(10)],
        'debit_potential': [random.randint(140, 200) for _ in range(10)],
        'energy_consumption': [random.randint(40, 60) for _ in range(10)],
        'energy_norm': [45 for _ in range(10)],
    }

    df = pd.DataFrame(wells_data)

    df['efficiency'] = (df['debit_fact'] / df['debit_potential'] * 100).round(1)
    df['oil_shortfall'] = (df['debit_potential'] - df['debit_fact']).round(1)
    df['energy_overuse'] = (df['energy_consumption'] - df['energy_norm']).round(1)

    return df


def analyze_wells(df):
    """Анализ показателей"""

    print("\n" + "=" * 60)
    print("АНАЛИЗ ЭФФЕКТИВНОСТИ СКВАЖИН")
    print("=" * 60)

    print("\n📊 Показатели:")
    print(df[['well_id', 'debit_fact', 'debit_potential', 'efficiency', 'oil_shortfall']].to_string(index=False))

    # Сохраняем
    df.to_excel(OUTPUT_DIR / 'well_analysis.xlsx', index=False)
    print(f"\n✅ Результаты сохранены")

    return df


def create_dashboard(df):
    """Дашборд"""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Мониторинг скважин - Газпром', fontsize=16)

    # График эффективности
    axes[0, 0].bar(df['well_id'], df['efficiency'], color='skyblue')
    axes[0, 0].axhline(y=70, color='red', linestyle='--', label='Порог 70%')
    axes[0, 0].set_title('Эффективность')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].legend()

    # Недобор
    axes[0, 1].bar(df['well_id'], df['oil_shortfall'], color='salmon')
    axes[0, 1].set_title('Недобор нефти')
    axes[0, 1].tick_params(axis='x', rotation=45)

    # Перерасход энергии
    axes[1, 0].bar(df['well_id'], df['energy_overuse'], color='lightgreen')
    axes[1, 0].set_title('Перерасход э/э')
    axes[1, 0].tick_params(axis='x', rotation=45)

    # Статистика
    stats = f"""
    Всего скважин: {len(df)}
    Средняя эффективность: {df['efficiency'].mean():.1f}%
    Скважин ниже 70%: {(df['efficiency'] < 70).sum()}
    Общий недобор: {df['oil_shortfall'].sum():.0f} т/сут
    """
    axes[1, 1].text(0.1, 0.5, stats, fontsize=14, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'dashboard.png', dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    df = create_sample_data()
    df = analyze_wells(df)
    create_dashboard(df)
    print("\n✅ Анализ завершён")