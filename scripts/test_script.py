import unittest
from unittest import mock
import argparse
from gh_cli import PrNotFoundException, GhCliException
import script
import subprocess

@mock.patch('script.argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(commit_sha='123', deploy_env='dev'))
@mock.patch('gh_cli.check_output')
@mock.patch('az_cli.check_output')
class TestTagging(unittest.TestCase):

    def test_should_properly_tag_ado_work_item_if_single_work_item_tag_in_pr_body(self, az_cli_check_output, gh_cli_check_output, parse_args_mock):
        gh_cli_check_output.return_value = '[{"body":"AB#123456"}]'
        
        script.main()
        
        gh_cli_check_output.assert_called_once_with('gh pr list --json body --state merged --search 123', shell=True, text=True, stderr=-2)
        az_cli_check_output.assert_called_once_with('az boards work-item update --id 123456 --org https://dev.azure.com/lukaszadamsielski0187 --fields "System.Tags=VNXT CL Dev"', shell=True, stderr=-2)
        
    def test_should_properly_tag_ado_work_items_if_many_work_item_tag_in_pr_body(self, az_cli_check_output, gh_cli_check_output, parse_args_mock):
        gh_cli_check_output.return_value = '[{"body":"AB#123456 AB#654321"}]'
        
        script.main()
        
        gh_cli_check_output.assert_called_once_with('gh pr list --json body --state merged --search 123', shell=True, text=True, stderr=-2)
        az_cli_check_output.assert_has_calls([
            mock.call('az boards work-item update --id 123456 --org https://dev.azure.com/lukaszadamsielski0187 --fields "System.Tags=VNXT CL Dev"', shell=True, stderr=-2),
            mock.call('az boards work-item update --id 654321 --org https://dev.azure.com/lukaszadamsielski0187 --fields "System.Tags=VNXT CL Dev"', shell=True, stderr=-2),
        ])
    
    def test_should_throw_exception_if_pr__not_found(self, az_cli_check_output, gh_cli_check_output, parse_args_mock):
        gh_cli_check_output.return_value = '[]'
        
        with self.assertRaises(PrNotFoundException) as e:
            script.main()
        self.assertEquals('Could not find pull request for commit identitifed by 123 SHA', str(e.exception))
        
    def test_should_throw_exception_if_gh_cli_command_failed(self, az_cli_check_output, gh_cli_check_output, parse_args_mock):
        gh_cli_check_output.side_effect = subprocess.CalledProcessError('test', 'test', 'Error!')
        
        with self.assertRaises(GhCliException) as e:
            script.main()
        self.assertEquals('Failed to execute GH CLI command! Error: Error!', str(e.exception))
