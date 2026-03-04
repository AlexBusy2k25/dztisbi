from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Создаем папку для output если её нет
OUTPUT_DIR.mkdir(exist_ok=True)


def analyze_well_metrics() -> None:
    """
    Анализ метрик эффективности работы скважин (аналог задачи 1).
    Рассчитывает коэффициенты эффективности и потери.
    """
    print("=" * 60)
    print("ЗАДАНИЕ 1: Анализ метрик работы скважин")
    print("=" * 60)

    # Создаем пример данных (в реальности здесь будет загрузка из Excel)
    wells_data = {
        'well_id': ['СКВ-001', 'СКВ-002', 'СКВ-003', 'СКВ-004', 'СКВ-005'],
        'debit_fact': [120, 85, 150, 90, 110],  # фактический дебит, т/сут
        'debit_potential': [150, 120, 160, 100, 130],  # потенциальный дебит, т/сут
        'energy_consumption': [45, 52, 48, 55, 50],  # кВт·ч/т
        'energy_norm': [40, 40, 45, 45, 42],  # норма, кВт·ч/т
        'oil_price': 50000,  # цена нефти, руб/т
        'energy_tariff': 5.5  # тариф на э/э, руб/кВт·ч
    }

    df = pd.DataFrame(wells_data)

    # Расчет метрик
    df['efficiency_coef'] = (df['debit_fact'] / df['debit_potential'] * 100).round(1)
    df['oil_shortfall'] = (df['debit_potential'] - df['debit_fact']).round(1)
    df['shortfall_losses'] = (df['oil_shortfall'] * df['oil_price']).round(0)
    df['energy_overuse'] = (df['energy_consumption'] - df['energy_norm']).round(1)
    df['energy_losses'] = (df['energy_overuse'] * df['debit_fact'] * df['energy_tariff']).round(0)

    print("\n📊 РАССЧИТАННЫЕ МЕТРИКИ:")
    print(df.to_string(index=False))

    # Сохраняем результаты
    df.to_excel(OUTPUT_DIR / 'well_metrics_result.xlsx', index=False)
    print(f"\n✅ Результаты сохранены в {OUTPUT_DIR / 'well_metrics_result.xlsx'}")

    return df


def analyze_reaction_time() -> None:
    """
    Анализ времени реакции на отклонения (аналог задачи 2).
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 2: Анализ времени реакции на отклонения")
    print("=" * 60)

    # Пример данных по инцидентам
    incidents = {
        'well_id': ['СКВ-001', 'СКВ-001', 'СКВ-002', 'СКВ-003', 'СКВ-004'],
        'date': ['2026-03-01', '2026-03-02', '2026-03-01', '2026-03-02', '2026-03-03'],
        'detection_time': [15, 10, 25, 20, 12],  # мин
        'reaction_time': [5, 8, 12, 10, 6],  # мин
        'diagnosis_time': [20, 15, 30, 25, 18],  # мин
        'instruction_time': [10, 10, 15, 12, 8],  # мин
        'execution_time': [45, 30, 60, 50, 35],  # мин
        'cause': ['засор', 'сбой', 'поломка', 'засор', 'сбой']
    }

    df = pd.DataFrame(incidents)

    # Расчет общего времени простоя
    df['total_downtime'] = (df['detection_time'] + df['reaction_time'] +
                            df['diagnosis_time'] + df['instruction_time'] +
                            df['execution_time'])

    # Агрегация по скважинам
    well_stats = df.groupby('well_id').agg({
        'total_downtime': ['mean', 'max', 'min'],
        'cause': lambda x: x.mode()[0] if not x.mode().empty else 'не определено'
    }).round(1)

    print("\n⏱️ СТАТИСТИКА ПО СКВАЖИНАМ:")
    print(well_stats.to_string())

    # Сохраняем
    df.to_excel(OUTPUT_DIR / 'reaction_time_result.xlsx', index=False)
    print(f"\n✅ Результаты сохранены в {OUTPUT_DIR / 'reaction_time_result.xlsx'}")


def create_dashboard_prototype() -> None:
    """
    Создание прототипа дашборда (визуализация метрик).
    """
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 3: Прототип дашборда")
    print("=" * 60)

    # Создаем фигуру с несколькими графиками
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Прототип дашборда "Мехфонд - Мониторинг скважин"', fontsize=14)

    # Данные для графиков
    wells = ['СКВ-001', 'СКВ-002', 'СКВ-003', 'СКВ-004', 'СКВ-005']
    efficiency = [80, 71, 94, 90, 85]
    losses = [1.5, 2.1, 0.8, 1.2, 1.8]

    # График 1: Коэффициент эффективности
    axes[0, 0].bar(wells, efficiency, color='green', alpha=0.7)
    axes[0, 0].set_title('Коэффициент эффективности, %')
    axes[0, 0].set_ylabel('%')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # График 2: Потери от недобора
    axes[0, 1].bar(wells, losses, color='red', alpha=0.7)
    axes[0, 1].set_title('Потери от недобора, млн руб')
    axes[0, 1].set_ylabel('млн руб')
    axes[0, 1].tick_params(axis='x', rotation=45)

    # График 3: Время реакции (гистограмма)
    reaction_times = [25, 18, 37, 30, 20]
    axes[1, 0].hist(reaction_times, bins=5, color='blue', alpha=0.7)
    axes[1, 0].set_title('Распределение времени реакции')
    axes[1, 0].set_xlabel('минуты')
    axes[1, 0].set_ylabel('частота')

    # График 4: Динамика по месяцам
    months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май']
    monthly_losses = [420, 380, 350, 320, 300]
    axes[1, 1].plot(months, monthly_losses, marker='o', linewidth=2, color='purple')
    axes[1, 1].set_title('Динамика недоборов нефти')
    axes[1, 1].set_xlabel('месяц')
    axes[1, 1].set_ylabel('тонн')
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()

    # Сохраняем дашборд
    dashboard_path = OUTPUT_DIR / 'dashboard_prototype.png'
    plt.savefig(dashboard_path, dpi=100, bbox_inches='tight')
    print(f"✅ Дашборд сохранен в {dashboard_path}")

    # Показываем (если нужно)
    # plt.show()


if __name__ == "__main__":
    print("\n" + "🚀 ЗАПУСК АНАЛИЗА ДАННЫХ (ГАЗПРОМ)")
    print("=" * 60)

    # Выполняем все задачи
    df_metrics = analyze_well_metrics()
    analyze_reaction_time()
    create_dashboard_prototype()

    print("\n" + "=" * 60)
    print("✅ ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ")
    print(f"📁 Результаты в папке: {OUTPUT_DIR}")