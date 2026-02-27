"""
AI Agent Demo - 使用 AgentGuard SDK
演示如何使用 SDK 统一管理 LLM 调用和审批流程
"""
from agent import SimpleAgent


def main():
    """主函数"""
    print("=" * 60)
    print("AI Agent Demo - AgentGuard SDK 集成示例")
    print("=" * 60)
    print("\n输入 'quit' 或 'exit' 退出\n")

    # 初始化 Agent
    agent = SimpleAgent()

    # 对话循环
    while True:
        try:
            user_input = input("\n用户: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit']:
                print("\n再见！")
                break

            # Agent 处理
            agent.chat(user_input, True)

        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"\n错误: {e}")




if __name__ == "__main__":
    main()
