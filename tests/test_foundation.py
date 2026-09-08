from pathlib import Path
import pytest
from storage.project_store import PortableProject
from storage.filesystem import SafeFilesystem
from core.security_pipeline import GuardedExecutionPipeline,RateLimit
from core.context import ApplicationContext
from models.entities import TargetScope,CommandSpec
from core.exceptions import PolicyViolation

def test_project_is_portable(tmp_path):
    project=PortableProject.create(tmp_path/'program','Demo','Bug Bounty');project.append('targets',{'target':'127.0.0.1'});assert list(project.read('targets'))[0]['target']=='127.0.0.1';assert (tmp_path/'program/project.json').exists()

def test_filesystem_blocks_escape(tmp_path):
    fs=SafeFilesystem(tmp_path)
    with pytest.raises(PermissionError):fs.resolve('../outside')

def test_pipeline_blocks_out_of_scope(tmp_path):
    context=ApplicationContext(tmp_path);pipeline=GuardedExecutionPipeline(context.executor);scope=TargetScope(['127.0.0.1'])
    with pytest.raises(PolicyViolation):pipeline.execute(CommandSpec('nmap',['-sn','example.com']),'example.com',scope)

def test_rate_limit():
    limit=RateLimit(1);assert limit.allow();assert not limit.allow()

