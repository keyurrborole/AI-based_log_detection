import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser

def test_parser():
    parser = LogParser()
    
    # Test 1: Failed login
    log1 = "Jan 10 10:21:44 server1 sshd[12345]: Failed password for root from 192.168.1.10"
    result1 = parser.parse_syslog(log1)
    
    print("✅ Test 1: Failed Login")
    assert result1['event_type'] == 'LOGIN_FAILURE'
    assert result1['user'] == 'root'
    assert result1['source_ip'] == '192.168.1.10'
    
    # Test 2: Successful login
    log2 = "Jan 10 10:25:00 server1 sshd[12350]: Accepted password for admin"
    result2 = parser.parse_syslog(log2)
    
    print("✅ Test 2: Successful Login")
    assert result2['event_type'] == 'LOGIN_SUCCESS'
    assert result2['user'] == 'admin'
    
    print("\n🎉 All parser tests passed!")

if __name__ == '__main__':
    test_parser()
