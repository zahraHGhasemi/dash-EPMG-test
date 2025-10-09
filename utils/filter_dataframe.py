
def filter_df_by_category(df, existing_words=[], non_existing_words=[]):
    filtered_df = df
    
    existing_words = [word.lower() for word in existing_words]
    non_existing_words = [word.lower() for word in non_existing_words]
    if existing_words:
        for word in existing_words:
            filtered_df = filtered_df[filtered_df['category'].apply(lambda x: any(word in item for item in x))]

    if non_existing_words:
        for word in non_existing_words:
            filtered_df = filtered_df[filtered_df['category'].apply(lambda x: not any(word in item for item in x))]
    return filtered_df