from src.modules.graph_conversion.entities import WorkFlow
import unittest

# Test Examples
class TestWorkFlow(unittest.TestCase):
    """
    Test workflow class based on modifications to check if the traits are being correctly calculated.
    """
    
    @staticmethod
    def create_workflow():
        workflow_example = WorkFlow()
        workflow_example.add_node(1, p=5)
        workflow_example.add_node(2, p=6)
        workflow_example.add_node(3, p=9)
        workflow_example.add_node(4, p=12)
        workflow_example.add_node(5, p=7)
        workflow_example.add_node(6, p=12)
        workflow_example.add_node(7, p=10)
        workflow_example.add_node(8, p=6)
        workflow_example.add_node(9, p=10)
        workflow_example.add_node(10, p=9)
        workflow_example.add_node(11, p=7)
        workflow_example.add_node(12, p=8)
        workflow_example.add_node(13, p=7)
        workflow_example.add_node(14, p=5)

        workflow_example.add_edges_from(
            [(1, 2), (2, 4), (4, 7), (7, 10), (10, 12), (12, 14)])
        workflow_example.add_edges_from(
            [(1, 3), (3, 6), (3, 5), (6, 9), (6, 8), (5, 9), (5, 8), (9, 11), (8, 11)])
        workflow_example.add_edges_from([(11, 12), (11, 13), (13, 14)])

        return workflow_example

    def reset(self):
        self.workflow = self.create_workflow()

    def test_original_makespan(self):
        self.reset()
        self.assertEqual(self.workflow.makespan, 56)

    def test_original_criticalpath(self):
        self.reset()
        self.assertEqual(list(self.workflow.critical_path.nodes()), [1, 3, 6, 9, 11, 12, 14])

    def test_modification_makespan(self):
        self.reset()
        # Add Edges
        self.workflow.add_edge(7, 3)
        self.assertEqual(self.workflow.makespan, 84)
        # Add Node
        self.workflow.add_node(5, p=20)
        self.assertEqual(self.workflow.makespan, 92)
        # Remove Edge
        self.workflow.remove_edge(7, 3)
        self.assertEqual(self.workflow.makespan, 64)
        # Remove Node
        self.workflow.remove_node(5)
        self.assertEqual(self.workflow.makespan, 56)

    def test_modification_criticalpath(self):
        self.reset()
        # Add Edges
        self.workflow.add_edge(7, 3)
        self.assertEqual(list(self.workflow.critical_path.nodes()), [1, 2, 3, 4, 6, 7, 9, 11, 12, 14])
        # Add Node
        self.workflow.add_node(5, p=20)
        self.assertEqual(list(self.workflow.critical_path.nodes()), [1, 2, 3, 4, 5, 7, 9, 11, 12, 14])
        # Remove Edge
        self.workflow.remove_edge(7, 3)
        self.assertEqual(list(self.workflow.critical_path.nodes()), [1, 3, 5, 9, 11, 12, 14])
        # Remove Node
        self.workflow.remove_node(5)
        self.assertEqual(list(self.workflow.critical_path.nodes()), [1, 3, 6, 9, 11, 12, 14])


if __name__ == '__main__':
    unittest.main()