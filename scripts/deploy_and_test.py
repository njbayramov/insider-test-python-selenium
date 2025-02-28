import subprocess
import time
import argparse

# Function to execute a shell command
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {e.stderr.decode('utf-8')}")
        return None

# Function to check if a Kubernetes service exists
def service_exists(service_name):
    command = f"kubectl get svc {service_name} --no-headers"
    result = run_command(command)
    return bool(result)

# Function to deploy a Kubernetes service
def deploy_service(service_name, yaml_file):
    print(f"🚀 Deploying service {service_name}...")
    run_command(f"kubectl apply -f {yaml_file}")
    
    # Wait for service to exist
    for attempt in range(10):
        output = run_command(f"kubectl get svc {service_name} --no-headers")
        if output:
            print(f"✅ Service {service_name} is now available.")
            return True
        print(f"⏳ Waiting for service {service_name} to be ready... (Attempt {attempt + 1}/10)")
        time.sleep(5)
    
    print(f"❌ Service {service_name} did not become available.")
    return False

# Function to check if a Kubernetes deployment is running
def is_deployment_running(deployment_name):
    command = f"kubectl get deployment {deployment_name} -o jsonpath='{{.status.availableReplicas}}'"
    result = run_command(command)
    return result and result.isdigit() and int(result) > 0

# Function to deploy a Kubernetes deployment
def deploy_deployment(deployment_name, yaml_file, retries=3, wait_time=5):
    for attempt in range(1, retries + 1):
        print(f"🚀 Deploying {deployment_name} (Attempt {attempt}/{retries})...")
        run_command(f"kubectl apply -f {yaml_file}")
        print(f"⏳ Waiting for {deployment_name} to reach Running state...")

        for _ in range(12):  # Max wait time: 12 * 5s = 60 seconds
            if is_deployment_running(deployment_name):
                print(f"✅ {deployment_name} is now Running.")
                return True
            time.sleep(wait_time)

        print(f"❌ {deployment_name} did not reach Running state, retrying...")
        run_command(f"kubectl delete -f {yaml_file}")
        time.sleep(wait_time)

    print(f"❌ {deployment_name} failed to start after {retries} attempts.")
    return False

# Function to check if an HPA exists
def hpa_exists(hpa_name):
    command = f"kubectl get hpa {hpa_name} --no-headers"
    result = run_command(command)
    return bool(result)

# Function to deploy an HPA
def deploy_hpa(hpa_name, yaml_file):
    print(f"🚀 Deploying HPA {hpa_name}...")
    run_command(f"kubectl apply -f {yaml_file}")
    
    # Wait for HPA to exist
    for attempt in range(10):
        output = run_command(f"kubectl get hpa {hpa_name} --no-headers")
        if output:
            print(f"✅ HPA {hpa_name} is now available.")
            return True
        print(f"⏳ Waiting for HPA {hpa_name} to be ready... (Attempt {attempt + 1}/10)")
        time.sleep(5)
    
    print(f"❌ HPA {hpa_name} did not become available.")
    return False

# Function to scale the chrome-node deployment
def scale_chrome_node(node_count):
    print(f"📏 Scaling chrome-node to {node_count} replicas...")
    command = f"kubectl scale deployment chrome-node --replicas={node_count}"
    if run_command(command):
        print(f"✅ Successfully scaled chrome-node to {node_count} replicas.")
    else:
        print(f"❌ Failed to scale chrome-node.")

# Function to check if the chrome-node pod is healthy
def is_chrome_node_healthy():
    print(f"🔍 Checking if chrome-node pod is healthy...")
    for attempt in range(10):
        command = "kubectl get pod -l app=chrome-node -o jsonpath='{.items[0].status.phase}'"
        status = run_command(command)
        if status == "Running":
            print(f"✅ Chrome-node pod is healthy.")
            return True
        print(f"⏳ Waiting for chrome-node pod to become healthy... (Attempt {attempt + 1}/10)")
        time.sleep(5)

    print(f"❌ Chrome-node pod is not healthy.")
    return False

# Function to get the actual pod name of the test controller pod
def get_test_controller_pod_name():
    command = "kubectl get pods -l app=selenium-test-controller -o jsonpath='{.items[0].metadata.name}'"
    pod_name = run_command(command)
    return pod_name

# Function to copy tests to the test controller pod
def copy_tests_to_test_controller():
    print(f"📂 Copying tests to selenium-test-controller pod...")
    pod_name = get_test_controller_pod_name()

    if pod_name:
        command = f"kubectl cp tests {pod_name}:/tests"
        result = run_command(command)

        if result is not None:
            print(f"✅ Tests copied successfully.")
        else:
            print(f"❌ Failed to copy tests.")
            exit(1)  # Exit the script if copying tests fails
    else:
        print(f"❌ No selenium-test-controller pod found.")
        exit(1)  # Exit the script if the pod isn't found

# Function to run tests inside the test controller pod
def run_tests():
    print(f"🧪 Running tests inside selenium-test-controller pod...")

    # Get the actual pod name of the test controller
    pod_name = get_test_controller_pod_name()

    if pod_name:
        # Run the tests using pytest inside the pod and capture the output
        command = ["kubectl", "exec", "-it", pod_name, "--", "pytest", "-v", "-s", "/tests/insider"]
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Print the test output and errors
        print("\n========= Test Output =========")
        print(result.stdout)
        print("========= Test Errors =========")
        print(result.stderr)

        # Check if the tests were successful or not based on the return code
        if result.returncode == 0:
            print(f"✅ Tests completed successfully.")
        else:
            print(f"❌ Tests failed.")
    else:
        print(f"❌ No selenium-test-controller pod found.")

# Function to print a separator
def print_separator():
    print("\n" + "=" * 50 + "\n")

# Main script execution
def main():
    parser = argparse.ArgumentParser(description="Deploy Kubernetes services, deployments, and run tests.")
    parser.add_argument("--node_count", type=int, default=1, help="Number of chrome-node replicas (min: 1, max: 5)")
    args = parser.parse_args()

    if args.node_count < 1 or args.node_count > 5:
        print(f"❌ Error: Invalid node_count '{args.node_count}'. Allowed range: 1 to 5.")
        exit(1)

    node_count = args.node_count

    print_separator()
    print("🔧 Kubernetes Service and Deployment Script")
    print_separator()

    # Step 1: Deploy services
    services = [
        {"name": "chrome-node", "file": "kubernetes/services/chrome-node.yaml"},
        {"name": "selenium-hub", "file": "kubernetes/services/selenium-hub.yaml"},
    ]

    for service in services:
        deploy_service(service["name"], service["file"])
    
    print_separator()

    # Step 2: Deploy deployments
    deployments = [
        {"name": "chrome-node", "file": "kubernetes/deployments/chrome-node.yaml"},
        {"name": "selenium-hub", "file": "kubernetes/deployments/selenium-hub.yaml"},
        {"name": "selenium-test-controller", "file": "kubernetes/deployments/selenium-test-controller.yaml"},
    ]

    for deployment in deployments:
        if not deploy_deployment(deployment["name"], deployment["file"]):
            print("❌ Stopping further deployments due to failure.")
            return

    print_separator()

    # Step 3: Scale chrome-node
    scale_chrome_node(node_count)

    print_separator()

    # Step 4: Deploy HPA
    deploy_hpa("chrome-node-hpa", "kubernetes/deployments/chrome-node-hpa.yaml")

    print_separator()
    print("🎉 All services, deployments, and HPA have been successfully deployed!")
    print_separator()

    # Step 5: Testing Section
    print("🧪 **Starting Tests**")
    print_separator()

    if not is_chrome_node_healthy():
        print("❌ Chrome-node pod is not healthy. Aborting tests.")
        return

    copy_tests_to_test_controller()
    run_tests()

    print_separator()
    print("✅ **Testing Completed!**")
    print_separator()

if __name__ == "__main__":
    main()
