import pytest
from core.policy_engine import ScopeEngine, AuthorizationEngine, PolicyEngine, RateLimitEngine, SecurityBoundary
from core.exceptions import PolicyViolation, ScopeError
from models.entities import Authorization, TargetScope

def test_scope_exclusion_wins():
    engine=ScopeEngine(['example.com','*.example.com'],['admin.example.com'])
    engine.check('www.example.com')
    with pytest.raises(ScopeError): engine.check('admin.example.com')

def test_intrusive_requires_authorized_lab():
    with pytest.raises(PolicyViolation): AuthorizationEngine().check(True)
    AuthorizationEngine(Authorization.AUTHORIZED,True).check(True)

def test_denied_operation():
    with pytest.raises(PolicyViolation): PolicyEngine().check('counter_attack')

def test_rate_limit_engine():
    rate=RateLimitEngine(1);assert rate.allow(10);assert not rate.allow(10)

def test_security_boundary():
    boundary=SecurityBoundary.from_target_scope(TargetScope(['127.0.0.1']))
    boundary.validate('127.0.0.1')
    with pytest.raises(PolicyViolation): boundary.validate('127.0.0.1','ddos')
