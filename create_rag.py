from knowledge_base_creation_pipeline import KnowledgeBaseCreationPipeline


def main() : 
    KBCPipeline = KnowledgeBaseCreationPipeline("pdfs")
    KBCPipeline.execute()

if __name__ == "__main__":
    main()

    

