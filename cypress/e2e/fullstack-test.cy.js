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
        cy.get('[data-cy="Imaging modality-categorical-field"]').click();
        cy.get('[role="listbox"]').contains("T1 Weighted");
        cy.get('[data-cy="Imaging modality-categorical-field"]').click();

        cy.get('[data-cy="Diagnosis-categorical-field"]').click();
        // We sadly can only select the expanded dropdown fields based on this role attribute
        // But both the parent and the dropdown field itself have the same role, so we need
        // to select them in this chained manner.
        // We only need to do this role=presentation selection if the dropdown elements are emtpy
        // otherwise we can do the more straightforward selection of role=listbox
        cy.get('[role="listbox"]')
            .within(() => {
                const terms = ["Attention deficit hyperactivity disorder"]
                terms.forEach(term => (
                    cy.contains(term, {matchCase: false})
                )
            )});
        cy.get('[data-cy="Diagnosis-categorical-field"]').click();

        cy.get('[data-cy="Assessment tool-categorical-field"]').click();
        cy.get('[role="listbox"]')
            .within(() => {
                const terms = ["Montreal cognitive assessment", "Unified Parkinsons disease rating scale score"]
                terms.forEach(term => (
                    cy.contains(term, {matchCase: false})
                )
            )});
        cy.get('[data-cy="Assessment tool-categorical-field"]').click();

        // cy.get('[role="menu"]')  // This is the typical role for a dropdown menu in MUI
        // .should('be.visible')  // Ensure the dropdown is visible
        // .within(() => {
        //   // Check if specific items are present
        //   cy.contains('Item 1').should('exist');  // Replace with your expected item text
        //   cy.contains('Item 2').should('exist');  // Replace with your expected item text
        //   cy.contains('Item 3').should('exist');  // Replace with your expected item text
        // });

    });
});