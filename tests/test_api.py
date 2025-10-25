import requests
import json
import time
from datetime import datetime

BASE_URL = 'http://localhost:8000/api/v1'
SERVER_URL = 'http://localhost:8000'

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def test_server_connection():
    print("\n" + "=" * 60)
    print("🔌 Testing Server Connection")
    print("=" * 60)
    
    try:
        response = requests.get(f'{SERVER_URL}/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Server is running")
            print_info(f"Status: {data.get('status')}")
            print_info(f"API Version: {data.get('api_version')}")
            return True
        else:
            print_error(f"Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server")
        print_warning("Make sure the server is running: python api/app.py")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_offices_api():
    print("\n" + "=" * 60)
    print("🏢 Testing Offices API")
    print("=" * 60)
    
    try:
        print("\n[Test 1] GET /offices")
        response = requests.get(f'{BASE_URL}/offices')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        print_success(f"Retrieved {data['total']} offices")
        
        if data['offices']:
            office = data['offices'][0]
            print_info(f"Sample office: {office['name']} ({office['country']})")
            
            print(f"\n[Test 2] GET /offices/{office['id']}")
            response = requests.get(f"{BASE_URL}/offices/{office['id']}")
            assert response.status_code == 200
            
            office_detail = response.json()
            print_success(f"Retrieved office details: {office_detail['name']}")
            print_info(f"Location: {office_detail['city']}, {office_detail['country']}")
            print_info(f"Region: {office_detail['region']}")
            print_info(f"Coordinates: {office_detail['coordinates']}")
            
            print(f"\n[Test 3] GET /offices/{office['id']}/devices")
            response = requests.get(f"{BASE_URL}/offices/{office['id']}/devices")
            assert response.status_code == 200
            
            devices_data = response.json()
            print_success(f"Office has {devices_data['total_devices']} devices")
            
            if devices_data['devices']:
                device = devices_data['devices'][0]
                print_info(f"Sample device: {device['name']} ({device['type']})")
        
        print("\n[Test 4] GET /offices?region=Africa")
        response = requests.get(f'{BASE_URL}/offices?region=Africa')
        assert response.status_code == 200
        
        africa_data = response.json()
        print_success(f"Found {africa_data['total']} offices in Africa")
        
        print_success("All Offices API tests passed")
        return True
        
    except AssertionError as e:
        print_error(f"Assertion failed: {e}")
        return False
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def test_devices_api():
    """测试设备API"""
    print("\n" + "=" * 60)
    print("🖥️  Testing Devices API")
    print("=" * 60)
    
    try:
        print("\n[Test 1] GET /devices")
        response = requests.get(f'{BASE_URL}/devices')
        assert response.status_code == 200
        
        data = response.json()
        print_success(f"Retrieved {data['total']} devices")
        
        if data['devices']:
            device = data['devices'][0]
            device_id = device['id']
            
            print_info(f"Sample device: {device['name']} ({device['type']})")
            
            print(f"\n[Test 2] GET /devices/{device_id}")
            response = requests.get(f"{BASE_URL}/devices/{device_id}")
            assert response.status_code == 200
            
            device_detail = response.json()
            print_success(f"Retrieved device details")
            print_info(f"IP: {device_detail.get('ip_address')}")
            print_info(f"Status: {device_detail.get('status')}")
            
            print(f"\n[Test 3] GET /devices/{device_id}/metrics")
            response = requests.get(f"{BASE_URL}/devices/{device_id}/metrics?hours=24")
            assert response.status_code == 200
            
            metrics = response.json()
            print_success(f"Retrieved {metrics['data_points']} metric data points")
            print_info(f"Period: {metrics['period']}")
            
            print(f"\n[Test 4] GET /devices/{device_id}/status")
            response = requests.get(f"{BASE_URL}/devices/{device_id}/status")
            assert response.status_code == 200
            
            status = response.json()
            print_success(f"Device health: {status['health_status']}")
            print_info(f"CPU: {status['metrics'].get('cpu_usage')}%")
            print_info(f"Memory: {status['metrics'].get('memory_usage')}%")
            
            if status['warnings']:
                print_warning(f"Warnings: {', '.join(status['warnings'])}")
            
            print(f"\n[Test 5] GET /devices/{device_id}/alerts")
            response = requests.get(f"{BASE_URL}/devices/{device_id}/alerts")
            assert response.status_code == 200
            
            alerts = response.json()
            print_success(f"Retrieved {alerts['total_alerts']} alerts")
        
        print("\n[Test 6] GET /devices?type=router")
        response = requests.get(f'{BASE_URL}/devices?type=router')
        assert response.status_code == 200
        
        routers = response.json()
        print_success(f"Found {routers['total']} routers")
        
        print_success("All Devices API tests passed")
        return True
        
    except AssertionError as e:
        print_error(f"Assertion failed: {e}")
        return False
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def test_analytics_api():
    print("\n" + "=" * 60)
    print("📊 Testing Analytics API")
    print("=" * 60)
    
    try:
        print("\n[Test 1] GET /analytics/summary")
        response = requests.get(f'{BASE_URL}/analytics/summary')
        assert response.status_code == 200
        
        summary = response.json()
        print_success("Retrieved global summary")
        
        health = summary['global_health']
        print_info(f"Offices: {health['active_offices']}/{health['total_offices']} active ({health['office_health']}%)")
        print_info(f"Devices: {health['online_devices']}/{health['total_devices']} online ({health['device_health']}%)")
        
        alerts = summary['alerts']
        print_info(f"Alerts: {alerts['critical']} critical, {alerts['warning']} warning, {alerts['info']} info")
        
        print("\n[Test 2] GET /analytics/region/Africa")
        response = requests.get(f'{BASE_URL}/analytics/region/Africa')
        assert response.status_code == 200
        
        region_data = response.json()
        print_success(f"Retrieved analytics for {region_data['region']}")
        print_info(f"Offices: {region_data['summary']['total_offices']}")
        print_info(f"Devices: {region_data['summary']['total_devices']}")
        print_info(f"Uptime: {region_data['performance']['average_uptime_pct']}%")
        
        print("\n[Test 3] GET /analytics/alerts")
        response = requests.get(f'{BASE_URL}/analytics/alerts?limit=10')
        assert response.status_code == 200
        
        alerts_data = response.json()
        print_success(f"Retrieved {alerts_data['total']} alerts")
        print_info(f"Critical: {alerts_data['critical_count']}")
        print_info(f"Warning: {alerts_data['warning_count']}")
        print_info(f"Info: {alerts_data['info_count']}")
        
        print("\n[Test 4] GET /analytics/trends?days=7")
        response = requests.get(f'{BASE_URL}/analytics/trends?days=7')
        assert response.status_code == 200
        
        trends = response.json()
        print_success(f"Retrieved {trends['data_points']} trend data points")
        print_info(f"Period: {trends['period_days']} days")
        
        print("\n[Test 5] GET /analytics/top-performers")
        response = requests.get(f'{BASE_URL}/analytics/top-performers?limit=5')
        assert response.status_code == 200
        
        performers = response.json()
        print_success(f"Retrieved top {len(performers['performers'])} performers")
        
        if performers['performers']:
            top = performers['performers'][0]
            print_info(f"Top performer: {top['device_name']} - {top['uptime_pct']}% uptime")
        
        print("\n[Test 6] GET /analytics/device-distribution")
        response = requests.get(f'{BASE_URL}/analytics/device-distribution')
        assert response.status_code == 200
        
        distribution = response.json()
        print_success(f"Device types: {distribution['types_count']}")
        for item in distribution['distribution']:
            print_info(f"  {item['type']}: {item['count']} ({item['percentage']}%)")
        
        print("\n[Test 7] GET /analytics/health-score")
        response = requests.get(f'{BASE_URL}/analytics/health-score')
        assert response.status_code == 200
        
        health_score = response.json()
        print_success(f"Health Score: {health_score['health_score']} - {health_score['status'].upper()}")
        print_info(f"Status: {health_score['status_icon']} {health_score['status']}")
        print_info(f"Recommendations: {len(health_score['recommendations'])}")
        
        print("\n[Test 8] POST /analytics/reports/generate")
        report_data = {
            'type': 'summary',
            'user': 'test_user',
            'include_trends': True,
            'include_alerts': True
        }
        response = requests.post(f'{BASE_URL}/analytics/reports/generate', json=report_data)
        assert response.status_code == 201
        
        report_response = response.json()
        print_success(f"Report generated: {report_response['report_id']}")
        
        report_id = report_response['report_id']
        
        print(f"\n[Test 9] GET /analytics/reports/{report_id}")
        response = requests.get(f"{BASE_URL}/analytics/reports/{report_id}")
        assert response.status_code == 200
        
        report = response.json()
        print_success(f"Retrieved report")
        print_info(f"Type: {report['type']}")
        print_info(f"Generated by: {report['generated_by']}")
        
        print_success("All Analytics API tests passed")
        return True
        
    except AssertionError as e:
        print_error(f"Assertion failed: {e}")
        return False
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def test_external_api():
    print("\n" + "=" * 60)
    print("🌐 Testing External API Integration")
    print("=" * 60)
    
    try:
        response = requests.get(f'{BASE_URL}/offices')
        offices = response.json()['offices']
        
        if not offices:
            print_warning("No offices available for external API testing")
            return True
        
        office = offices[0]
        office_id = office['id']
        
        print(f"\n[Test 1] GET /external/weather/{office_id}")
        response = requests.get(f"{BASE_URL}/external/weather/{office_id}")
        
        if response.status_code == 200:
            weather = response.json()
            print_success(f"Retrieved weather for {weather['office_name']}")
            weather_data = weather['weather']
            print_info(f"Temperature: {weather_data.get('temperature')}°C")
            print_info(f"Description: {weather_data.get('description')}")
            print_info(f"Humidity: {weather_data.get('humidity')}%")
        else:
            print_warning(f"Weather API returned {response.status_code}")
        
        print(f"\n[Test 2] GET /external/time/{office_id}")
        response = requests.get(f"{BASE_URL}/external/time/{office_id}")
        
        if response.status_code == 200:
            time_data = response.json()
            print_success(f"Retrieved time info for {time_data['office_name']}")
            time_info = time_data['time_info']
            print_info(f"Timezone: {time_info.get('timezone')}")
            print_info(f"Local time: {time_info.get('datetime')}")
        else:
            print_warning(f"Time API returned {response.status_code}")
        
        country_code = office.get('country', 'KE')[:2]  
        print(f"\n[Test 3] GET /external/country/{country_code}")
        response = requests.get(f"{BASE_URL}/external/country/{country_code}")
        
        if response.status_code == 200:
            country_info = response.json()
            print_success(f"Retrieved country info")
            print_info(f"Name: {country_info.get('name')}")
            print_info(f"Capital: {country_info.get('capital')}")
            print_info(f"Population: {country_info.get('population'):,}")
        else:
            print_warning(f"Country API returned {response.status_code}")
        
        if len(offices) >= 2:
            print("\n[Test 4] GET /external/distance")
            office1_id = offices[0]['id']
            office2_id = offices[1]['id']
            response = requests.get(f"{BASE_URL}/external/distance?office1={office1_id}&office2={office2_id}")
            
            if response.status_code == 200:
                distance_data = response.json()
                print_success(f"Distance calculated")
                print_info(f"{distance_data['office1']['name']} → {distance_data['office2']['name']}")
                print_info(f"Distance: {distance_data['distance_km']} km")
        
        print_success("All External API tests passed")
        return True
        
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def test_performance():
    print("\n" + "=" * 60)
    print("⚡ Testing API Performance")
    print("=" * 60)
    
    endpoints = [
        ('GET /offices', f'{BASE_URL}/offices'),
        ('GET /devices', f'{BASE_URL}/devices'),
        ('GET /analytics/summary', f'{BASE_URL}/analytics/summary'),
        ('GET /analytics/alerts', f'{BASE_URL}/analytics/alerts?limit=10'),
        ('GET /analytics/trends', f'{BASE_URL}/analytics/trends?days=7'),
    ]
    
    results = []
    
    for name, url in endpoints:
        try:
            requests.get(url, timeout=5)
            
            times = []
            for _ in range(3):
                start = time.time()
                response = requests.get(url, timeout=5)
                duration = (time.time() - start) * 1000
                
                if response.status_code == 200:
                    times.append(duration)
            
            avg_time = sum(times) / len(times) if times else 0
            
            print(f"\n{name}")
            print_info(f"  Average response time: {avg_time:.2f}ms")
            
            if avg_time < 100:
                print_success(f"  Excellent performance")
            elif avg_time < 500:
                print_info(f"  Good performance")
            elif avg_time < 1000:
                print_warning(f"  Acceptable performance")
            else:
                print_error(f"  Slow response time")
            
            results.append({
                'endpoint': name,
                'avg_time_ms': round(avg_time, 2),
                'status': 'pass' if avg_time < 1000 else 'slow'
            })
            
        except Exception as e:
            print_error(f"  Failed: {e}")
            results.append({
                'endpoint': name,
                'status': 'failed',
                'error': str(e)
            })
    
    print("\n" + "-" * 60)
    passed = sum(1 for r in results if r.get('status') == 'pass')
    print(f"Performance Summary: {passed}/{len(results)} endpoints under 1s")
    
    return all(r.get('status') != 'failed' for r in results)

def run_all_tests():
    print("\n")
    print("=" * 60)
    print("🧪 UNDP ICT Dashboard API Test Suite")
    print("=" * 60)
    print(f"Target: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = {}
    
    if not test_server_connection():
        print("\n" + "=" * 60)
        print_error("Cannot proceed without server connection")
        print("=" * 60)
        return
    
    results['offices'] = test_offices_api()
    results['devices'] = test_devices_api()
    results['analytics'] = test_analytics_api()
    results['external'] = test_external_api()
    results['performance'] = test_performance()
    
    print("\n" + "=" * 60)
    print("📋 Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        color = Colors.GREEN if passed else Colors.RED
        print(f"{color}{test_name.capitalize():20s}: {status}{Colors.END}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print_success("All tests passed! 🎉")
    else:
        failed_count = sum(1 for passed in results.values() if not passed)
        print_error(f"{failed_count} test suite(s) failed")
    print("=" * 60)
    
    return all_passed

if __name__ == '__main__':
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        exit(1)