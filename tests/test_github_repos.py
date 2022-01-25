""" Test suite for Github /repos """
from unittest import TestCase, skip
from apis.github.repos import Repos
from utilities.config import Config


class TestGithubRepos(TestCase):
    """ Test class for Github /repos """

    def test_github_repos_successful_response(self):
        """
        Test for Github /repos successful response

        Asserts /repos response contains successful status code and contains all expected attributes
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute()
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        keys = [
            'id', 'node_id', 'name', 'full_name', 'private', 'owner', 'html_url', 'description', 'fork', 'url',
            'forks_url', 'keys_url', 'collaborators_url', 'teams_url', 'hooks_url', 'issue_events_url', 'events_url',
            'assignees_url', 'branches_url', 'tags_url', 'blobs_url', 'git_tags_url', 'git_refs_url', 'trees_url',
            'statuses_url', 'languages_url', 'stargazers_url', 'contributors_url', 'subscribers_url',
            'subscription_url', 'commits_url', 'git_commits_url', 'comments_url', 'issue_comment_url', 'contents_url',
            'compare_url', 'merges_url', 'archive_url', 'downloads_url', 'issues_url', 'pulls_url', 'milestones_url',
            'notifications_url', 'labels_url', 'releases_url', 'deployments_url', 'created_at', 'updated_at',
            'pushed_at', 'git_url', 'ssh_url', 'clone_url', 'svn_url', 'homepage', 'size', 'stargazers_count',
            'watchers_count', 'language', 'has_issues', 'has_projects', 'has_downloads', 'has_wiki', 'has_pages',
            'forks_count', 'mirror_url', 'archived', 'disabled', 'open_issues_count', 'license', 'allow_forking',
            'is_template', 'topics', 'visibility', 'forks', 'open_issues', 'watchers', 'default_branch']
        owner_keys = [
            'login', 'id', 'node_id', 'avatar_url', 'gravatar_id', 'url', 'html_url', 'followers_url', 'following_url',
            'gists_url', 'starred_url', 'subscriptions_url', 'organizations_url', 'repos_url', 'events_url',
            'received_events_url', 'type', 'site_admin']

        json_response = response.json()
        for repo in json_response:
            for key in keys:
                self.assertIn(key, repo, "'" + key + "' missing from Github /repos response")
            for key in owner_keys:
                self.assertIn(key, repo['owner'], "'owner[" + key + "]' missing from Github /repos response")

    def test_github_repos_type_owner(self):
        """
        Test for Github /repos with type=owner

        Asserts /repos response contains successful status code and that the owner of the repos is the expected owner
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(repo_type="owner")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        user = Config().get_json("users")["candidate"]
        owner_id = 7978671

        json_response = response.json()
        for repo in json_response:
            owner = repo['owner']
            self.assertTrue(
                owner['login'] == user and owner['id'] == owner_id,
                "Github /repos returned repos of different users when type=owner: "
                "'" + owner['login'] + "' and '" + user + "' and " +
                "'" + str(owner['id']) + "' and '" + str(owner_id) + "'")

    @skip("Lack of a user that is only a member to a repo")
    def test_github_repos_type_member(self):
        """
        Test for Github /repos with type=member

        Asserts /repos response contains successful status code and that the owner of the repos is the expected owner
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(repo_type="member")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        # TODO: Find a user that is a member of a repo they don't own or join a repo as a member with existing user

    def test_github_repos_type_all(self):
        """
        Test for Github /repos with type=all

        Asserts /repos response contains successful status code and it pull all repos of the user
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(repo_type="all")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        total_repos = len(response.json())

        owner_response = github_repos_endpoint.execute(repo_type="owner")
        owner_json_response = owner_response.json()
        member_response = github_repos_endpoint.execute(repo_type="member")
        member_json_response = member_response.json()
        total_owner_and_member_repos = len(set(
            [repo['id'] for repo in owner_json_response] + [repo['id'] for repo in member_json_response]))
        self.assertEqual(total_repos, total_owner_and_member_repos, "Github /repos type=all did not return all repos")

    def test_github_repos_type_unknown(self):
        """
        Test for Github /repos with type=unknown

        Asserts /repos response contains successful status code and it defaults to owner
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(repo_type="unknown")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        user = Config().get_json("users")["candidate"]
        owner_id = 7978671

        json_response = response.json()
        for repo in json_response:
            owner = repo['owner']
            self.assertTrue(
                owner['login'] == user and owner['id'] == owner_id,
                "Github /repos returned repos of different users when type=owner: "
                "'" + owner['login'] + "' and '" + user + "' and " +
                "'" + str(owner['id']) + "' and '" + str(owner_id) + "'")

    def test_github_repos_sort_full_name(self):
        """
        Test for Github /repos with sort=full_name

        Asserts /repos response contains successful status code and it sorts by the full_name attribute
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(sort="full_name")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        json_response = response.json()
        repo_sorted_by_full_names = [repo['full_name'] for repo in json_response]
        for i in range(1, len(repo_sorted_by_full_names)):
            self.assertLess(repo_sorted_by_full_names[i - 1].lower(), repo_sorted_by_full_names[i].lower(),
                            "Github /repos not sorted by full_name")

    @skip("Actually broken on github!!!")
    def test_github_repos_sort_created(self):
        """
        Test for Github /repos with sort=created

        Asserts /repos response contains successful status code and it sorts by the created_at attribute
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(sort="created")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        json_response = response.json()
        repo_sorted_by_created = [repo['created_at'] for repo in json_response]
        for i in range(1, len(repo_sorted_by_created)):
            self.assertLess(repo_sorted_by_created[i - 1].lower(), repo_sorted_by_created[i].lower(),
                            "Github /repos not sorted by created_at")

    @skip("Actually broken on github!!!")
    def test_github_repos_sort_updated(self):
        """
        Test for Github /repos with sort=updated

        Asserts /repos response contains successful status code and it sorts by the updated_at attribute
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(sort="updated")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        json_response = response.json()
        repo_sorted_by_updated = [repo['updated_at'] for repo in json_response]
        for i in range(1, len(repo_sorted_by_updated)):
            self.assertLess(repo_sorted_by_updated[i - 1].lower(), repo_sorted_by_updated[i].lower(),
                            "Github /repos not sorted by updated_at")

    @skip("Actually broken on github!!!")
    def test_github_repos_sort_pushed(self):
        """
        Test for Github /repos with sort=pushed

        Asserts /repos response contains successful status code and it sorts by the pushed_at attribute
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(sort="updated")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        json_response = response.json()
        repo_sorted_by_pushed = [repo['pushed_at'] for repo in json_response]
        for i in range(1, len(repo_sorted_by_pushed)):
            self.assertLess(repo_sorted_by_pushed[i - 1].lower(), repo_sorted_by_pushed[i].lower(),
                            "Github /repos not sorted by pushed_at")

    def test_github_repos_sort_unknown(self):
        """
        Test for Github /repos with sort=unknown

        Asserts /repos response contains successful status code and it sorts by the default full_name attribute
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(sort="unknown")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        json_response = response.json()
        repo_sorted_by_full_names = [repo['full_name'] for repo in json_response]
        for i in range(1, len(repo_sorted_by_full_names)):
            self.assertLess(repo_sorted_by_full_names[i - 1].lower(), repo_sorted_by_full_names[i].lower(),
                            "Github /repos not sorted by full_name")

    def test_github_repos_direction_asc(self):
        """
        Test for Github /repos with direction=asc

        Asserts /repos response contains successful status code and it sorts by the full_name attribute ascending
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(direction="asc")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        json_response = response.json()
        repo_sorted_by_full_names = [repo['full_name'] for repo in json_response]
        for i in range(1, len(repo_sorted_by_full_names)):
            self.assertLess(repo_sorted_by_full_names[i - 1].lower(), repo_sorted_by_full_names[i].lower(),
                            "Github /repos not sorted by full_name in ascending direction")

    @skip("Actually broken on github!!!")
    def test_github_repos_direction_desc(self):
        """
        Test for Github /repos with direction=desc

        Asserts /repos response contains successful status code and it sorts by the full_name attribute descending
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(direction="desc")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        json_response = response.json()
        repo_sorted_by_full_names = [repo['full_name'] for repo in json_response]
        for i in range(1, len(repo_sorted_by_full_names)):
            self.assertGreater(repo_sorted_by_full_names[i - 1].lower(), repo_sorted_by_full_names[i].lower(),
                            "Github /repos not sorted by full_name in ascending direction")

    def test_github_repos_direction_unknown(self):
        """
        Test for Github /repos with direction=unknown

        Asserts /repos response contains successful status code and it sorts by the full_name attribute default
         ascending
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(direction="unknown")
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        json_response = response.json()
        repo_sorted_by_full_names = [repo['full_name'] for repo in json_response]
        for i in range(1, len(repo_sorted_by_full_names)):
            self.assertLess(repo_sorted_by_full_names[i - 1].lower(), repo_sorted_by_full_names[i].lower(),
                            "Github /repos not sorted by default full_name in ascending direction")

    @skip("Actually broken on github!!!")
    def test_github_repos_per_page_1(self):
        """
        Test for Github /repos with per_page=1

        Asserts /repos response contains successful status code and only returns 1 repo
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(per_page=1)
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        self.assertEqual(len(response.json()), 1, "Github /repos did not return the correct number of repos")

    def test_github_repos_per_page_1000(self):
        """
        Test for Github /repos with per_page=1000

        Asserts /repos response contains successful status code and only returns default 30 repos per page
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(per_page=1000)
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        # only have 5 repos to test with
        self.assertEqual(len(response.json()), 5, "Github /repos did not return the correct number of repos")

    @skip("Need user with a lot of repos and for per_page to work")
    def test_github_repos_page_5(self):
        """
        Test for Github /repos with page=5

        Asserts /repos response contains successful status code and only returns 5 pages of repos
        """
        github_repos_endpoint = Repos(user="candidate")
        response = github_repos_endpoint.execute(page=5)
        self.assertEqual(response.status_code, 200, "Github /repos unsuccessfully fetched response")

        # TODO - Find user with a lot of repos, 30 * pages to test
