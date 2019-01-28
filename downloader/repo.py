class Repo():
    def __init__(self, slug, repo_id, repo_name, state, project_id, forkable=True):
        self.slug = slug
        self.repo_id = repo_id
        self.repo_name = repo_name
        self.state = state
        self.project_id = project_id
        self.forkable = forkable