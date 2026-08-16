
from backend.services.agent import AutomotiveDefectAgent


def main():

    agent = AutomotiveDefectAgent()

    result = agent.analyze(
        defect="scratch",
        confidence=0.91
    )

    print("\n================================")
    print("AUTOMOTIVE AI QUALITY ANALYSIS")
    print("================================")

    print("\nDEFECT:")
    print(result["defect"])

    print("\nCONFIDENCE:")
    print(f"{result['confidence']:.2%}")

    print("\nAI ANALYSIS:")
    print(result["analysis"])

    print("\nRAG SOURCES:")

    for source in result["sources"]:
        print(source[:150])
        print("--------------------------------")


if __name__ == "__main__":
    main()