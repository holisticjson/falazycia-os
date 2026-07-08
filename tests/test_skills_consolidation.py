import os

def test_skills_consolidation_count():
    """Verify that there are exactly 22 skill folders in the skills directory."""
    skills_dir = r"c:\Aplikacje MVP\Holistic Jason\skills"
    assert os.path.exists(skills_dir), "Skills directory does not exist"
    
    subdirs = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    assert len(subdirs) == 22, f"Expected exactly 22 skill folders, got {len(subdirs)}"

def test_skills_contain_skill_md():
    """Verify that every skill folder contains a SKILL.md file."""
    skills_dir = r"c:\Aplikacje MVP\Holistic Jason\skills"
    subdirs = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    
    for subdir in subdirs:
        skill_md_path = os.path.join(skills_dir, subdir, "SKILL.md")
        assert os.path.exists(skill_md_path), f"SKILL.md missing in {subdir}"

def test_director_skills_are_present():
    """Verify that the 11 director skills are all present in the skills directory."""
    director_skills = {
        "cco", "ceo", "cfo", "cmo", "coo", "cso", "cto",
        "generate-video-reel", "ghost", "hermes-cloud-architect-sop", "holistic"
    }
    skills_dir = r"c:\Aplikacje MVP\Holistic Jason\skills"
    subdirs = set(d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d)))
    
    missing_directors = director_skills - subdirs
    assert not missing_directors, f"Missing director skills: {missing_directors}"
