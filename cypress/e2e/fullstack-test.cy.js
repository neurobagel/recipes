// This test ensures that the query tool works correctly with the entire stack of running services.
// If this test fails, we will need to check the individual service to service interfaces to find the bug.

describe('When I load the query tool', () => {
    it('I am greeted by a functioning UI without warnings', () => {
        // Visit the site
        cy.visit('http://localhost:3000/')
        
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
});