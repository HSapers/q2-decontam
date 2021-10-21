import somestuff

# We hand decontam an FT of all features in all samples within group

def filter_to_one_group_and_run_decontam_to_score(ctx,
    ft: FeatureTable, md: Metadata, some_col: MetadataColumn, grp: str,
        ) -> decontam.Scores:
    # filter to one group
    filter = ctx.get_action('feature-table', 'filter-features')
    feats = filter(ft, md, where='some_col==grp')
    # Run decontam to scores
    # return {group_id: Scores}

def build_FTs_for_each_unique_group_in_metadata(
    ft: FeatureTable, md: Metadata, cols: List[MetadataColumns],
        ) -> :
    # Find all unique groups and assign unique ids like colheader_value

    all_scores = dict()
    for group_id in groups:
        id, scores = filter_to_one_group_and_run_decontam_to_score(ft, md)
        all_scores[id] = scores

    # write one file to our DirectoryFormat for each id ||
    # build a table using the scores and IDs ||
    # ?
    # Return whatever data structure you decide to implement
