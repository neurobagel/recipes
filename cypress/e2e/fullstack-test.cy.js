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
    it('I see the expected options for each variable dropdown', () => {
        // In this test we're looking at dropdown items in the expanded dropdown area.
        // 
        // There are no good selectors for the expanded dropdown area.
        // What's more: if the dropdown is empty, it will have the attribute role=presentation,
        // but if it has items, it will have the attribute role=listbox. We make use of this
        // here by only selecting for role=listbox - the test will fail if the dropdown is empty
        // either way, but now it will fail because the element is not found.

        // Sex
        // Sex is hardcoded, so we don't have to check for each option to exist
        cy.get('[data-cy="Sex-categorical-field"]').click();
        cy.get('[role="listbox"]').contains("male");
        cy.get('[data-cy="Sex-categorical-field"]').click();

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
        
        // Imaging modality
        cy.get('[data-cy="Imaging modality-categorical-field"]').click();
        cy.get('[role="listbox"]').contains("T1 Weighted");
        cy.get('[data-cy="Imaging modality-categorical-field"]').click();

        // Pipeline Name
        cy.get('[data-cy="Pipeline name-categorical-field"]').click();
        cy.get('[role="listbox"]')
            .within(() => {
                const terms = ["Freesurfer", "fmriprep"]
                terms.forEach(term => (
                    cy.contains(term, {matchCase: false})
                )
            )});
        cy.get('[data-cy="Pipeline name-categorical-field"]').click();
    });
});
describe.only('When I run an unfiltered query on all nodes', () => {
    beforeEach(() => {
        cy.visit('http://localhost:3000/')
    });
    it('I see the expected matching datasets', () => {
        cy.get('[data-cy="Neurobagel graph-categorical-field"]').type(
            'local graph 1{downarrow}{enter}'
        );
        cy.get('[data-cy="submit-query-button"]').click();
        cy.get('[data-cy="summary-stats"]').contains("1 datasets");
        cy.get('[data-cy="result-container"]')
            .within(() => {
                const substrings = ["BIDS synthetic", "Local graph 1", "5 subjects match", "5 total subjects", "Flow", "T1"]
                substrings.forEach(substring => (
                    cy.contains(substring, {matchCase: false})
                )
            )});
        cy.contains("button", "Available pipelines").trigger("mouseover")
        cy.get('.MuiTooltip-tooltip')
            .within(() => {
                ["fmriprep 23.1.3", "freesurfer 7.3.2"].forEach(pipeline => (
                    cy.contains(pipeline, {matchCase: false})
                )
            )});
    });
});