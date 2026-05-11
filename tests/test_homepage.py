import pytest
from app.homepage import app, format_uptime, get_deployment_info


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestRoutes:
    """Test Flask routes"""

    def test_homepage_status_code(self, client):
        """Test homepage returns 200"""
        response = client.get('/')
        assert response.status_code == 200

    def test_homepage_contains_content(self, client):
        """Test homepage contains expected content"""
        response = client.get('/')
        assert b'DevOps' in response.data or b'Profile' in response.data

    def test_health_endpoint(self, client):
        """Test /health endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_api_status_endpoint(self, client):
        """Test /api/status endpoint returns deployment info"""
        response = client.get('/api/status')
        assert response.status_code == 200
        data = response.get_json()
        assert 'version' in data
        assert 'environment' in data
        assert 'status' in data

    def test_api_projects_endpoint(self, client):
        """Test /api/projects endpoint"""
        response = client.get('/api/projects')
        assert response.status_code == 200
        data = response.get_json()
        assert 'projects' in data
        assert len(data['projects']) > 0

    def test_profile_route_valid(self, client):
        """Test /profile/<name> route with valid profile"""
        response = client.get('/profile/yourname')
        assert response.status_code == 200

    def test_profile_route_invalid(self, client):
        """Test /profile/<name> route with invalid profile"""
        response = client.get('/profile/nonexistent')
        assert response.status_code == 200
        assert b'Not Found' in response.data


class TestUtilityFunctions:
    """Test utility functions"""

    def test_format_uptime_seconds(self):
        """Test format_uptime with seconds only"""
        result = format_uptime(45)
        assert '45s' in result

    def test_format_uptime_minutes(self):
        """Test format_uptime with minutes and seconds"""
        result = format_uptime(125)
        assert 'm' in result and 's' in result

    def test_format_uptime_hours(self):
        """Test format_uptime with hours"""
        result = format_uptime(3665)
        assert 'h' in result

    def test_get_deployment_info_structure(self):
        """Test get_deployment_info returns correct structure"""
        info = get_deployment_info()
        required_keys = ['version', 'deploy_number', 'environment', 'status', 'last_deploy', 'uptime']
        for key in required_keys:
            assert key in info
