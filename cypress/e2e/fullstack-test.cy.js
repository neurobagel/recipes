// This test ensures that the query tool works correctly with the entire stack of running services.
// If this test fails, we will need to check the individual service to service interfaces to find the bug.

describe('When I load the query tool', () => {
    beforeEach(() => {
        cy.visit('http://localhost:3000/')
    });
    it('I am greeted by a functioning UI without warnings', () => {
        
        cy.get('[data-cy="navbar"]').contains('Neurobagel')
        // Click the node dropdown and assert that the items contain the node names we expect
        cy.get('[data-cy="Neurobagel graph-categorical-field"]').type(
            'local graph 1{downarrow}{enter}'
          );
        // get list element and check that it contains the expected node names
        cy.get('[data-cy="Neurobagel graph-categorical-field"]').contains("Local graph 1")
        // Click the bell icon and then check that the Warning area is empty
        cy.get('[data-cy="notification-button"]').click();
        cy.get('li').contains("No notifications");
        cy.get('body').click();
    });
    it.only('I see the expected options for each variable dropdown', () => {
        // In this test we're looking at dropdown items in the expanded dropdown area.
        // 
        // There are no good selectors for the expanded dropdown area.
        // What's more: if the dropdown is empty, it will have the attribute role=presentation,
        // but if it has items, it will have the attribute role=listbox. We make use of this
        // here by only selecting for role=listbox - the test will fail if the dropdown is empty
        // either way, but now it will fail because the element is not found.

        // Imaging modality
        cy.get('[data-cy="Imaging modality-categorical-field"]').click();
        cy.get('[role="listbox"]').contains("T1 Weighted");
        cy.get('[data-cy="Imaging modality-categorical-field"]').click();

        // Diagnosis
        cy.get('[data-cy="Diagnosis-categorical-field"]').click();       
        cy.get('[role="listbox"]')
            .within(() => {
                const terms = ["Attention deficit hyperactivity disorder"]
                terms.forEach(term => (
                    cy.contains(term, {matchCase: false})
                )
            )});
        cy.get('[data-cy="Diagnosis-categorical-field"]').click();

        // Assessment tool
        cy.get('[data-cy="Assessment tool-categorical-field"]').click();
        cy.get('[role="listbox"]')
            .within(() => {
                const terms = ["Montreal cognitive assessment", "Unified Parkinsons disease rating scale score"]
                terms.forEach(term => (
                    cy.contains(term, {matchCase: false})
                )
            )});
        cy.get('[data-cy="Assessment tool-categorical-field"]').click();

    });
});