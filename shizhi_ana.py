import numpy as np
import matplotlib.pyplot as plt


# 获取股票滚动市盈率


def main():
    # 输入数据
    data_input = input("Enter data separated by spaces: ")
    data = list(map(float, data_input.split()))
    
    # 输入分桶数量
    k = int(input("Enter the number of bins: "))
    
    # 计算分界点，确保包含最大值
    min_val = min(data)
    max_val = max(data)
    epsilon = 1e-8  # 防止因浮点精度问题导致最大值被排除
    max_val += epsilon
    width = (max_val - min_val) / k
    bins = [min_val + i * width for i in range(k + 1)]
    
    # 统计每个桶的频率
    counts, _ = np.histogram(data, bins=bins)
    
    # 计算均值和标准差
    mean_val = np.mean(data)
    std_val = np.std(data)
    
    # 输出结果
    print("\nBucket Boundaries:")
    print(bins)
    
    print("\nFrequencies per Bucket:")
    for i in range(k):
        print(f"Bucket {i+1}: [{bins[i]:.4f}, {bins[i+1]:.4f}) has {counts[i]} elements")
    
    print(f"\nEstimated Mean: {mean_val:.4f}")
    print(f"Estimated Standard Deviation: {std_val:.4f}")
    
    # 绘制图表
    plt.figure(figsize=(12, 6))
    plt.plot(data, marker='o', linestyle='-', linewidth=2, markersize=8, label='Original Data')
    
    # 绘制均线（均值水平线）
    plt.axhline(y=mean_val, color='r', linestyle='--', linewidth=2, label='Mean')
    
    # 绘制±1标准差虚线
    upper = mean_val + std_val
    lower = mean_val - std_val
    plt.axhline(y=upper, color='g', linestyle=':', linewidth=2, label='+1σ')
    plt.axhline(y=lower, color='g', linestyle=':', linewidth=2, label='-1σ')
    
    # 图表装饰
    plt.title('Data Distribution with Mean and ±1σ Boundaries')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()