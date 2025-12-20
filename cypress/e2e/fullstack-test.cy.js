// This test ensures that the query tool works correctly with the entire stack of running services.
// If this test fails, we will need to check the individual service to service interfaces to find the bug.

describe('When I load the query tool', () => {
    beforeEach(() => {
        cy.visit('http://localhost:3000/')
    });
    it('I am greeted by a functioning UI without warnings', () => {
        
        cy.get('[data-cy="navbar"]').contains('Neurobagel')
        // Click the node dropdown and assert that the items contain the node names we expect
        cy.get('[data-cy="Neurobagel graph-categorical-field"]').click();
        // get list element and check that it contains the expected node names
        cy.get('[role="listbox"]').within(() => {
            ["2 OpenNeuro Datasets", "BIDS synthetic"].forEach(node => (
                cy.contains(node, {matchCase: false})
            ))});
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
        cy.get('[role="listbox"]').contains("T1-weighted image");
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

describe('When I run an unfiltered query on all nodes', () => {

    beforeEach(() => {
        // We need to include the ?node=All otherwise it seems the app switches URLs at some point
        // from http://localhost:3000/ to http://localhost:3000/?node=All,
        // which is registered as a modification to query fields, thus preventing the results download
        cy.visit('http://localhost:3000/?node=All')
        // Listen for f-API request so we can wait for it later before checking results
        cy.intercept('*datasets*').as('call');
        cy.get('[data-cy="submit-query-button"]').click();
    });
    
    it('I see the expected matching dataset info', () => {
        cy.get('[data-cy="summary-stats"]').contains("3 datasets");
        cy.get('[data-cy="result-container"]').within(() => {
            cy.get('[data-cy^="card-"]').contains("BIDS synthetic").closest('[data-cy^="card-"]').as("bidsSyntheticCard");
            cy.get("@bidsSyntheticCard").within(() => {
                const substrings = ["5 subjects match", "5 total subjects", "BOLD", "T1W"]
                substrings.forEach(substring => (
                    cy.contains(substring, {matchCase: false})
                ))
            });
            cy.contains("Balloon Analog Risk-taking Task", {matchCase: false});
            cy.contains("Classification learning", {matchCase: false});
        });
        cy.get("@bidsSyntheticCard").within(() => {
            cy.contains("button", "Available pipelines").trigger("mouseover");
        });
        // This must be outside of the dataset card selector because the tooltip exceeds the card boundaries (?)
        cy.get('.MuiTooltip-tooltip')
            .within(() => {
                ["fmriprep 23.1.3", "freesurfer 7.3.2"].forEach(pipeline => (
                    cy.contains(pipeline, {matchCase: false})
                )
            )});
    });
    
    // TODO: This test is currently blocked from passing by https://github.com/neurobagel/query-tool/issues/670
    // Undo skip when issue is resolved.
    it.skip('The results TSV I download contains the expected contents', () => {
        cy.wait('@call');
        cy.get('[data-cy="select-all-checkbox"]').find('input').check();
        cy.get('[data-cy="download-results-button"]').click();
        cy.readFile('cypress/downloads/neurobagel-query-results.tsv').then((fileContent) => {
          const rows = fileContent.split('\n');
          // TODO: Need to make case-insensitive?
          const openneuroDatasetProtected = rows.some(row => 
            row.includes("Classification learning") && row.includes("protected")
          );
          const syntheticDatasetOpen = rows.some(row => 
            row.includes("BIDS synthetic") && !row.includes("protected")
          );
          expect(openneuroDatasetProtected).to.be.true;
          expect(syntheticDatasetOpen).to.be.true;
        })
    });
});

describe('When I run a filtered query on all nodes', () => {
    it('I see the expected matching datasets and subjects', () => {
        cy.visit('http://localhost:3000/')
        cy.get('[data-cy="Minimum age-continuous-field"]').type('30');
        cy.get('[data-cy="Maximum age-continuous-field"]').type('45');
        cy.get('[data-cy="Sex-categorical-field"]').click();
        // We need to exact match "male" to avoid matching "female"
        cy.get("li").contains(/^male$/, {matchCase: false}).click();
        cy.get('[data-cy="Diagnosis-categorical-field"]').type('attention{downarrow}{enter}');
        cy.get('[data-cy="Minimum number of imaging sessions-continuous-field"]').type('1');
        cy.get('[data-cy="Minimum number of phenotypic sessions-continuous-field"]').type('1');
        cy.get('[data-cy="Assessment tool-categorical-field"]').type('montreal{downarrow}{enter}')
        cy.get('[data-cy="Imaging modality-categorical-field"]').type('t1{downarrow}{enter}')
        cy.intercept('/pipelines/np:freesurfer/versions').as('getPipelineVersionsOptions');
        cy.get('[data-cy="Pipeline name-categorical-field"]').type('freesurfer{downarrow}{enter}')
        cy.wait('@getPipelineVersionsOptions');
        cy.get('[data-cy="Pipeline version-categorical-field"]').type('7.3.2{downarrow}{enter}');
        cy.intercept('*datasets*').as('call');
        cy.get('[data-cy="submit-query-button"]').click();
        cy.wait('@call');
        
        cy.get('[data-cy="summary-stats"]').contains("1 datasets");
        cy.get('[data-cy="result-container"]')
            .within(() => {
                ["BIDS synthetic", "1 subjects match"].forEach(substring => (
                    cy.contains(substring, {matchCase: false})
                )
            )});
    });
});
