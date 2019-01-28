class PullRequest():
    def __init__(self, 
        pr_id, 
        version, 
        title, 
        desc, 
        state,
        creation_date, 
        update_date, 
        from_ref, 
        to_ref, 
        author_id, 
        reviewer_ids, 
        participant_ids, 
        link):
        self.pr_id = pr_id
        self.version = version
        self.title = title
        self.desc = desc
        self.state = state
        self.creation_date = creation_date
        self.update_date = update_date
        self.from_ref = from_ref
        self.to_ref = to_ref
        self.author_id = author_id
        self.reviewer_ids = reviewer_ids
        self.participant_ids = participant_ids
        self.link = link